# import frappe
# from mohan_impex.is_created import is_link_name_exists


# @frappe.whitelist()
# def pr_invoice(party_name=None, payment_type=None):
# 	party_name = (party_name or "").strip()
# 	payment_type = (payment_type or "").strip()

# 	mapping = {
# 		"Labour Payment": {
# 			"amount_field": "custom_total_labour_cost",
# 			"party_field": "contractors_name"
# 		},
# 		"Transporter Payment": {
# 			"amount_field": "transport_charges",
# 			"party_field": "transporter"
# 		},
# 		"Miscellaneous Payment": {
# 			"amount_field": "total_misc_amount",
# 			"party_field": "misc_supplier"
# 		}
# 	}

# 	if payment_type not in mapping:
# 		frappe.throw("Invalid payment_type")

# 	amount_field = mapping[payment_type]["amount_field"]
# 	party_field = mapping[payment_type]["party_field"]

# 	meta = frappe.get_meta("Purchase Receipt")

# 	# safety check
# 	if not meta.has_field(amount_field):
# 		frappe.throw(f"Field '{amount_field}' not found in Purchase Receipt")

# 	# fields to fetch
# 	fields = ["name", party_field, amount_field]

# 	if meta.has_field("posting_date"):
# 		fields.append("posting_date")
# 	if meta.has_field("custom_labour_rate"):
# 		fields.append("custom_labour_rate")
# 	if meta.has_field("supplier_name"):
# 		fields.append("supplier_name")

# 	filters = {"docstatus": 1, amount_field: (">", 0)}

# 	if party_name:
# 		filters[party_field] = party_name

# 	rows = frappe.db.get_all(
# 		"Purchase Receipt",
# 		filters=filters,
# 		fields=fields,
# 		order_by="posting_date desc"
# 	)

# 	result = []
# 	for r in rows:
# 		pr_name = r.get("name")
# 		amt = r.get(amount_field) or 0

# 		if amt <= 0:
# 			continue

# 		# skip already used PR
# 		if is_link_name_exists(pr_name, payment_type):
# 			continue

# 		# ✅ rate logic as requested
# 		if payment_type == "Labour Payment":
# 			rate = r.get("custom_labour_rate") or 0
# 		else:
# 			rate = amt

# 		result.append({
# 			"name": pr_name,
# 			"party_name": r.get("supplier_name") or r.get(party_field),
# 			"amount": amt,
# 			"payment_type": payment_type,
# 			"date": r.get("posting_date"),
# 			"rate": rate,
# 		})

# 	return result


import frappe
from frappe.utils import getdate
from mohan_impex.is_created import is_link_name_exists


def _get_link_doctype(meta, fieldname: str):
	df = meta.get_field(fieldname)
	if df and df.fieldtype == "Link" and df.options:
		return df.options
	return None


def _get_display_name(party_doctype: str, party_value: str, cache: dict):
	if not party_doctype or not party_value:
		return party_value

	key = (party_doctype, party_value)
	if key in cache:
		return cache[key]

	try:
		pmeta = frappe.get_meta(party_doctype)
	except Exception:
		cache[key] = party_value
		return party_value

	candidate_fields = [
		"supplier_name",
		"customer_name",
		"employee_name",
		"transporter_name",
		"contractor_name",
		"full_name",
		"title",
	]
	name_field = next((f for f in candidate_fields if pmeta.has_field(f)), None)

	if name_field:
		val = frappe.db.get_value(party_doctype, party_value, name_field) or party_value
	else:
		val = party_value

	cache[key] = val
	return val


def _validate_dates(from_date, to_date):
	if bool(from_date) ^ bool(to_date):
		frappe.throw("Both from_date and to_date are required.")

	if not from_date and not to_date:
		return None, None

	fd = getdate(from_date)
	td = getdate(to_date)

	if td < fd:
		frappe.throw("to_date cannot be before from_date.")

	return fd, td


@frappe.whitelist()
def pr_invoice(party_name=None, payment_type=None, from_date=None, to_date=None, limit=500):
	party_name = (party_name or "").strip()
	payment_type = (payment_type or "").strip()

	from_date, to_date = _validate_dates(from_date, to_date)

	mapping = {
		"Labour Payment": {
			"amount_field": "custom_total_labour_cost",
			"party_field": "contractors_name",
		},
		"Transporter Payment": {
			"amount_field": "transport_charges",
			"party_field": "transporter",
		},
		"Miscellaneous Payment": {
			"amount_field": "total_misc_amount",
			"party_field": "misc_supplier",
		},
	}

	if payment_type not in mapping:
		frappe.throw("Invalid payment_type")

	amount_field = mapping[payment_type]["amount_field"]
	party_field = mapping[payment_type]["party_field"]

	meta = frappe.get_meta("Purchase Receipt")

	for f in (amount_field, party_field):
		if not meta.has_field(f):
			frappe.throw(f"Field '{f}' not found in Purchase Receipt")

	fields = ["name", party_field, amount_field]

	# ✅ total_qty
	if meta.has_field("total_qty"):
		fields.append("total_qty")

	# date field + order_by (posting_date preferred)
	if meta.has_field("posting_date"):
		date_field = "posting_date"
		fields.append("posting_date")
		order_by = "posting_date desc"
	else:
		date_field = "modified"
		order_by = "modified desc"

	# labour rate
	if meta.has_field("custom_labour_rate"):
		fields.append("custom_labour_rate")

	filters = {"docstatus": 1, amount_field: (">", 0)}

	if party_name:
		filters[party_field] = party_name

	# ✅ date range filter
	if from_date and to_date:
		filters[date_field] = ["between", [from_date, to_date]]

	rows = frappe.db.get_all(
		"Purchase Receipt",
		filters=filters,
		fields=fields,
		order_by=order_by,
		limit_page_length=int(limit) if limit else 500,
	)

	party_doctype = _get_link_doctype(meta, party_field)
	party_name_cache = {}

	result = []
	for r in rows:
		pr_name = r.get("name")
		amt = r.get(amount_field) or 0
		if amt <= 0:
			continue

		if is_link_name_exists(pr_name, payment_type):
			continue

		party_value = r.get(party_field)
		display_party = _get_display_name(party_doctype, party_value, party_name_cache)

		# ✅ rate logic as requested
		if payment_type == "Labour Payment":
			rate = r.get("custom_labour_rate") or 0
		else:
			rate = amt

		result.append(
			{
				"name": pr_name,
				"party_name": display_party or party_value,
				"amount": amt,
				"payment_type": payment_type,
				"date": r.get(date_field),
				"rate": rate,
				"total_qty": r.get("total_qty") if "total_qty" in r else 0,
			}
		)

	return result
