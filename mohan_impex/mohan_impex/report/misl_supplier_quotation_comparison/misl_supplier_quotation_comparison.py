# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from collections import defaultdict

import frappe
from frappe import _
from frappe.utils import cint, flt, strip_html

from erpnext.buying.utils import get_last_purchase_details  # last purchase details


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns(filters)
	supplier_quotation_data = get_data(filters)

	data, chart_data = prepare_data(supplier_quotation_data, filters)
	message = get_message()

	return columns, data, message, chart_data


def validate_filters(filters):
	if not filters.get("categorize_by") and filters.get("group_by"):
		filters["categorize_by"] = filters["group_by"]
		filters["categorize_by"] = filters["categorize_by"].replace("Group by", "Categorize by")


def get_data(filters):
	sq = frappe.qb.DocType("Supplier Quotation")
	sq_item = frappe.qb.DocType("Supplier Quotation Item")

	query = (
		frappe.qb.from_(sq_item)
		.from_(sq)
		.select(
			sq_item.parent,
			sq_item.item_code,
			sq_item.item_name,
			sq_item.qty,
			sq.currency,
			sq_item.stock_qty,
			sq_item.amount,
			sq_item.base_rate,
			sq_item.base_amount,
			sq.price_list_currency,
			sq_item.uom,
			sq_item.stock_uom,
			sq_item.request_for_quotation,
			sq_item.lead_time_days,
			sq.supplier.as_("supplier_name"),
			sq.valid_till,
			sq.terms,  # Delivery terms (HTML from Quill)
		)
		.where(
			(sq_item.parent == sq.name)
			& (sq_item.docstatus < 2)
			& (sq.company == filters.get("company"))
			& (sq.transaction_date.between(filters.get("from_date"), filters.get("to_date")))
		)
		.orderby(sq.transaction_date, sq_item.item_code)
	)

	if filters.get("item_code"):
		query = query.where(sq_item.item_code == filters.get("item_code"))

	if filters.get("supplier_quotation"):
		query = query.where(sq_item.parent.isin(filters.get("supplier_quotation")))

	if filters.get("request_for_quotation"):
		query = query.where(sq_item.request_for_quotation == filters.get("request_for_quotation"))

	if filters.get("supplier"):
		query = query.where(sq.supplier.isin(filters.get("supplier")))

	if not filters.get("include_expired"):
		query = query.where(sq.status != "Expired")

	supplier_quotation_data = query.run(as_dict=True)

	return supplier_quotation_data


def prepare_data(supplier_quotation_data, filters):
	out, groups, qty_list, suppliers, chart_data = [], [], [], [], []
	group_wise_map = defaultdict(list)
	supplier_qty_price_map = {}

	group_by_field = (
		"supplier_name" if filters.get("categorize_by") == "Categorize by Supplier" else "item_code"
	)
	float_precision = cint(frappe.db.get_default("float_precision")) or 2

	# Cache last purchase details per item_code
	last_purchase_cache = {}
	# Cache payment terms per supplier
	payment_terms_cache = {}

	for data in supplier_quotation_data:
		group = data.get(group_by_field)
		item_code = data.get("item_code")
		supplier = data.get("supplier_name")

		# --- Last Purchase Details (cached per item_code) ---
		last_purchase_rate = None
		last_purchase_date = None

		if item_code:
			if item_code not in last_purchase_cache:
				try:
					details = get_last_purchase_details(item_code) or {}
				except Exception:
					details = {}
				last_purchase_cache[item_code] = details
			else:
				details = last_purchase_cache[item_code]

			rate_val = details.get("rate") or details.get("base_rate")
			last_purchase_rate = flt(rate_val, float_precision) if rate_val is not None else None
			last_purchase_date = details.get("purchase_date")

		# --- Payment Terms (cached per supplier) ---
		payment_terms = None
		if supplier:
			if supplier not in payment_terms_cache:
				payment_terms_cache[supplier] = frappe.db.get_value(
					"Supplier", supplier, "payment_terms"
				)
			payment_terms = payment_terms_cache[supplier]

		# --- Clean Delivery terms (strip HTML from Quill content) ---
		terms_html = data.get("terms") or ""
		if terms_html:
			# optional: add line breaks between paragraphs before stripping
			terms_html = terms_html.replace("</p>", "</p>\n")
			delivery_terms = strip_html(terms_html).replace("&nbsp;", " ").strip()
		else:
			delivery_terms = ""

		# Base values
		base_amount = flt(data.get("base_amount"), float_precision)
		base_rate = flt(data.get("base_rate"), float_precision)

		row = {
			"supplier_name": "" if group_by_field == "supplier_name" else supplier,
			"quotation": data.get("parent"),
			"item_code": "" if group_by_field == "item_code" else item_code,
			"item_name": data.get("item_name"),
			"qty": data.get("qty"),
			"uom": data.get("uom"),
			"price_per_unit_inr": base_rate,  # Price Per Unit (INR)
			"currency": data.get("currency"),
			"base_amount": base_amount,  # Price (INR)
			"lead_time_days": data.get("lead_time_days"),
			"terms": delivery_terms,  # ✅ cleaned plain-text Delivery terms
			"payment_terms": payment_terms,
			"last_purchase_rate": last_purchase_rate,
			"last_purchase_date": last_purchase_date,
			"valid_till": data.get("valid_till"),
			"request_for_quotation": data.get("request_for_quotation"),
		}

		# internal: for min-price highlighting & chart
		row["price"] = flt(data.get("amount"), float_precision)
		row["price_per_unit"] = flt(row["price"]) / (flt(data.get("stock_qty")) or 1)

		group_wise_map[group].append(row)

		if filters.get("item_code"):
			if supplier not in supplier_qty_price_map:
				supplier_qty_price_map[supplier] = {}
			supplier_qty_price_map[supplier][row["qty"]] = row["price"]

		groups.append(group)
		suppliers.append(supplier)
		qty_list.append(data.get("qty"))

	groups = list(set(groups))
	suppliers = list(set(suppliers))
	qty_list = list(set(qty_list))

	highlight_min_price = group_by_field == "item_code" or filters.get("item_code")

	# final data format for report view
	for group in groups:
		group_entries = group_wise_map[group]
		# ensure grouping field is visible in first row only
		group_entries[0].update({group_by_field: group})

		if highlight_min_price:
			prices = [ge["price_per_unit_inr"] for ge in group_entries]
			prices = [p for p in prices if p is not None]
			min_price = min(prices) if prices else None
		else:
			min_price = None

		for entry in group_entries:
			if highlight_min_price and min_price is not None and entry["price_per_unit_inr"] == min_price:
				entry["min"] = 1
			out.append(entry)

	if filters.get("item_code"):
		chart_data = prepare_chart_data(suppliers, qty_list, supplier_qty_price_map)
	else:
		chart_data = []

	return out, chart_data


def prepare_chart_data(suppliers, qty_list, supplier_qty_price_map):
	data_points_map = {}
	qty_list.sort()

	for supplier in suppliers:
		entry = supplier_qty_price_map.get(supplier, {})
		for qty in qty_list:
			if qty not in data_points_map:
				data_points_map[qty] = []
			if qty in entry:
				data_points_map[qty].append(entry[qty])
			else:
				data_points_map[qty].append(None)

	dataset = []
	currency_symbol = frappe.db.get_value("Currency", frappe.db.get_default("currency"), "symbol")
	for qty in qty_list:
		datapoints = {
			"name": currency_symbol + " (Qty " + str(qty) + " )",
			"values": data_points_map[qty],
		}
		dataset.append(datapoints)

	chart_data = {"data": {"labels": suppliers, "datasets": dataset}, "type": "bar"}

	return chart_data


def get_columns(filters):
	# Only the columns you requested, in your order.
	return [
		{
			"fieldname": "supplier_name",
			"label": _("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 150,
		},
		{
			"fieldname": "quotation",
			"label": _("Supplier Quotation"),
			"fieldtype": "Link",
			"options": "Supplier Quotation",
			"width": 180,
		},
		{
			"fieldname": "item_code",
			"label": _("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 140,
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "qty",
			"label": _("Quantity"),
			"fieldtype": "Float",
			"width": 90,
		},
		{
			"fieldname": "uom",
			"label": _("UOM"),
			"fieldtype": "Link",
			"options": "UOM",
			"width": 90,
		},
		{
			"fieldname": "price_per_unit_inr",
			"label": _("Price Per Unit (INR)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 140,
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 90,
		},
		{
			"fieldname": "base_amount",
			"label": _("Price (INR)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 130,
		},
		{
			"fieldname": "lead_time_days",
			"label": _("Lead Time (Days)"),
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"fieldname": "terms",
			"label": _("Delivery terms"),
			"fieldtype": "Text",
			"width": 260,
		},
		{
			"fieldname": "payment_terms",
			"label": _("Payment terms"),
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"fieldname": "last_purchase_rate",
			"label": _("Last Purchase Rate"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 130,
		},
		{
			"fieldname": "last_purchase_date",
			"label": _("Last Purchase Date"),
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"fieldname": "valid_till",
			"label": _("Valid Till"),
			"fieldtype": "Date",
			"width": 110,
		},
		{
			"fieldname": "request_for_quotation",
			"label": _("Request for Quotation"),
			"fieldtype": "Link",
			"options": "Request for Quotation",
			"width": 180,
		},
	]


def get_message():
	return f"""<span class="indicator">
		{_("Valid Till")}:&nbsp;&nbsp;
		</span>
		<span class="indicator orange">
		{_("Expires in a week or less")}
		</span>
		&nbsp;&nbsp;
		<span class="indicator red">
		{_("Expires today or already expired")}
		</span>"""


@frappe.whitelist()
def set_default_supplier(item_code, supplier, company):
	frappe.db.set_value(
		"Item Default",
		{"parent": item_code, "company": company},
		"default_supplier",
		supplier,
	)
