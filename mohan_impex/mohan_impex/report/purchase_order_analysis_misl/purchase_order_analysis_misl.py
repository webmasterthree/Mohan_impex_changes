import copy

import frappe
from frappe import _
from frappe.query_builder.functions import IfNull, Sum
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns(filters)
	data = get_data(filters)

	if not data:
		return [], [], None, []

	update_received_amount(data)
	update_gst_rate(data)

	data, chart_data = prepare_data(data, filters)

	return columns, data, None, chart_data


def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	# Require both dates if either is provided
	if (from_date and not to_date) or (to_date and not from_date):
		frappe.throw(_("From and To Dates are required."))

	if from_date and to_date and date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))


def get_data(filters):
	po = frappe.qb.DocType("Purchase Order")
	po_item = frappe.qb.DocType("Purchase Order Item")
	pi_item = frappe.qb.DocType("Purchase Invoice Item")

	query = (
		frappe.qb.from_(po)
		.inner_join(po_item)
		.on(po_item.parent == po.name)
		.left_join(pi_item)
		.on((pi_item.po_detail == po_item.name) & (pi_item.docstatus == 1))
		.select(
			po.transaction_date.as_("date"),
			po_item.schedule_date.as_("required_date"),
			po_item.project,
			po.name.as_("purchase_order"),
			po.status,
			po.supplier,
			po_item.item_code,
			po_item.qty,
			po_item.rate,
			po_item.item_tax_template,
			po_item.received_qty,
			(po_item.qty - po_item.received_qty).as_("pending_qty"),
			Sum(IfNull(pi_item.qty, 0)).as_("billed_qty"),
			po_item.base_amount.as_("amount"),
			(po_item.billed_amt * IfNull(po.conversion_rate, 1)).as_("billed_amount"),
			(po_item.base_amount - (po_item.billed_amt * IfNull(po.conversion_rate, 1))).as_(
				"pending_amount"
			),
			po.set_warehouse.as_("warehouse"),
			po.company,
			po.total_taxes_and_charges,
			po.grand_total,
			po.tc_name,
			po_item.name,
		)
		.where((po.status.notin(("Stopped", "On Hold"))) & (po.docstatus == 1))
		.groupby(po_item.name)
		.orderby(po.transaction_date)
	)

	if filters.get("company"):
		query = query.where(po.company == filters.get("company"))

	if filters.get("name"):
		query = query.where(po.name.isin(filters.get("name")))

	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(po.transaction_date.between(filters.get("from_date"), filters.get("to_date")))

	if filters.get("status"):
		query = query.where(po.status.isin(filters.get("status")))

	if filters.get("project"):
		query = query.where(po_item.project == filters.get("project"))

	return query.run(as_dict=True)


def update_received_amount(data):
	pr_data = get_received_amount_data(data)

	for row in data:
		row["received_qty_amount"] = flt(pr_data.get(row.name))


def get_received_amount_data(data):
	pr = frappe.qb.DocType("Purchase Receipt")
	pr_item = frappe.qb.DocType("Purchase Receipt Item")

	po_items = [row.name for row in data]
	if not po_items:
		return frappe._dict()

	query = (
		frappe.qb.from_(pr)
		.inner_join(pr_item)
		.on(pr_item.parent == pr.name)
		.select(
			pr_item.purchase_order_item,
			Sum(pr_item.base_amount).as_("received_qty_amount"),
		)
		.where((pr.docstatus == 1) & (pr_item.purchase_order_item.isin(po_items)))
		.groupby(pr_item.purchase_order_item)
	)

	result = query.run()
	if not result:
		return frappe._dict()

	return frappe._dict(result)


def update_gst_rate(data):
	"""Attach gst_rate from Item Tax Template to each row (bulk lookup)."""
	templates = sorted({row.get("item_tax_template") for row in data if row.get("item_tax_template")})

	if not templates:
		for row in data:
			row["gst_rate"] = 0.0
		return

	rows = frappe.get_all(
		"Item Tax Template",
		filters={"name": ["in", templates]},
		fields=["name", "gst_rate"],
	)

	template_map = {d["name"]: flt(d.get("gst_rate")) for d in rows}

	for row in data:
		row["gst_rate"] = template_map.get(row.get("item_tax_template"), 0.0)


def prepare_data(data, filters):
	completed, pending = 0, 0
	pending_field = "pending_amount"
	completed_field = "billed_amount"

	purchase_order_map = {} if filters.get("group_by_po") else None

	for row in data:
		# sum data for chart
		completed += flt(row.get(completed_field))
		pending += flt(row.get(pending_field))

		# qty to bill
		row["qty_to_bill"] = flt(row.get("qty")) - flt(row.get("billed_qty"))

		# Dynamic GST computation (for non-grouped view; harmless to compute always)
		base_amount = flt(row.get("amount"))
		gst_rate = flt(row.get("gst_rate"))  # percent e.g. 12.0
		row["gst_amount"] = base_amount * (gst_rate / 100.0)
		row["amount_with_gst"] = base_amount + row["gst_amount"]

		if filters.get("group_by_po"):
			po_name = row.get("purchase_order")

			if po_name not in purchase_order_map:
				row_copy = copy.deepcopy(row)
				purchase_order_map[po_name] = row_copy
			else:
				po_row = purchase_order_map[po_name]

				# required_date = earliest required date (handle None safely)
				existing_date = po_row.get("required_date")
				new_date = row.get("required_date")
				if existing_date and new_date:
					po_row["required_date"] = min(getdate(existing_date), getdate(new_date))
				else:
					po_row["required_date"] = existing_date or new_date

				# sum numeric columns (do NOT show GST cols when grouped, but safe to keep computed)
				fields = [
					"qty",
					"received_qty",
					"pending_qty",
					"billed_qty",
					"qty_to_bill",
					"amount",
					"received_qty_amount",
					"billed_amount",
					"pending_amount",
				]
				for field in fields:
					po_row[field] = flt(row.get(field)) + flt(po_row.get(field))

	chart_data = prepare_chart_data(pending, completed)

	if filters.get("group_by_po"):
		data = [purchase_order_map[po] for po in purchase_order_map]
		return data, chart_data

	return data, chart_data


def prepare_chart_data(pending, completed):
	labels = [_("Amount to Bill"), _("Billed Amount")]

	return {
		"data": {"labels": labels, "datasets": [{"values": [pending, completed]}]},
		"type": "donut",
		"height": 300,
	}


def get_columns(filters):
	is_grouped = bool(filters.get("group_by_po"))

	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 90},
		{"label": _("Required By"), "fieldname": "required_date", "fieldtype": "Date", "width": 90},
		{
			"label": _("Purchase Order"),
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 160,
		},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 130},
		{
			"label": _("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 130,
		},
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 130,
		},
	]

	# Item Code only when not grouped
	if not is_grouped:
		columns.append(
			{
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 100,
			}
		)

	# Rate always
	columns.append(
		{
			"label": _("Rate"),
			"fieldname": "rate",
			"fieldtype": "Currency",
			"width": 120,
			"convertible": "rate",
		}
	)

	# GST Rate ONLY when not grouped
	if not is_grouped:
		columns.append(
			{
				"label": _("GST Rate"),
				"fieldname": "gst_rate",
				"fieldtype": "Percent",
				"width": 90,
			}
		)

	columns.extend(
		[
			{
				"label": _("Qty"),
				"fieldname": "qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Received Qty"),
				"fieldname": "received_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Pending Qty"),
				"fieldname": "pending_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Billed Qty"),
				"fieldname": "billed_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Qty to Bill"),
				"fieldname": "qty_to_bill",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Amount"),
				"fieldname": "amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
		]
	)
	if is_grouped:
		columns.extend(
			[
				{
					"label": _("Total GST Amount"),
					"fieldname": "total_taxes_and_charges",
					"fieldtype": "Currency",
				},
				{
					"label": _("Total  Amount (Incl GST)"),
					"fieldname": "grand_total",
					"fieldtype": "Currency",
				},
				{
					"label": _("Delivery Terms"),
					"fieldname": "tc_name",
					"fieldtype": "Link",
					"options":"Terms and Conditions"
				}
			]
		)

	# GST Amount + Amount (Incl GST) ONLY when not grouped
	if not is_grouped:
		columns.extend(
			[
				{
					"label": _("GST Amount"),
					"fieldname": "gst_amount",
					"fieldtype": "Currency",
					"width": 130,
					"options": "Company:company:default_currency",
					"convertible": "rate",
				},
				{
					"label": _("Amount (Incl GST)"),
					"fieldname": "amount_with_gst",
					"fieldtype": "Currency",
					"width": 160,
					"options": "Company:company:default_currency",
					"convertible": "rate",
				},
			]
		)

	columns.extend(
		[
			{
				"label": _("Billed Amount"),
				"fieldname": "billed_amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Pending Amount"),
				"fieldname": "pending_amount",
				"fieldtype": "Currency",
				"width": 130,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Received Qty Amount"),
				"fieldname": "received_qty_amount",
				"fieldtype": "Currency",
				"width": 130,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Warehouse"),
				"fieldname": "warehouse",
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 100,
			},
			{
				"label": _("Company"),
				"fieldname": "company",
				"fieldtype": "Link",
				"options": "Company",
				"width": 100,
			},
		]
	)

	return columns
