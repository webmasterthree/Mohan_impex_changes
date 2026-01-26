# import frappe
# from mohan_impex.is_created import is_link_name_exists


# @frappe.whitelist()
# def dn_invoice(party_name=None, payment_type=None):
# 	party_name = (party_name or "").strip()
# 	payment_type = (payment_type or "").strip()

# 	mapping = {
# 		"Labour Payment": {
# 			"amount_field": "custom_total_labour_cost",
# 			"party_field": "contractors_name"
# 		},
# 		"Transporter Payment": {
# 			"amount_field": "custom_transport_charges",
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

# 	meta = frappe.get_meta("Delivery Note")

# 	# safety check for dynamic amount field
# 	if not meta.has_field(amount_field):
# 		frappe.throw(f"Field '{amount_field}' not found in Delivery Note")

# 	# fields to fetch (safe)
# 	fields = ["name", party_field, amount_field]

# 	if meta.has_field("posting_date"):
# 		fields.append("posting_date")
# 	if meta.has_field("customer_name"):
# 		fields.append("customer_name")
# 	if meta.has_field("custom_labour_rate"):
# 		fields.append("custom_labour_rate")

# 	filters = {"docstatus": 1, amount_field: (">", 0)}

# 	# party filter if provided (kept as-is)
# 	if party_name:
# 		filters[party_field] = party_name

# 	rows = frappe.db.get_all(
# 		"Delivery Note",
# 		filters=filters,
# 		fields=fields,
# 		order_by="posting_date desc"
# 	)

# 	result = []
# 	for r in rows:
# 		dn_name = r.get("name")
# 		amt = r.get(amount_field) or 0

# 		if amt <= 0:
# 			continue

# 		# skip already linked in Purchase Invoice for same service_payment_type
# 		if is_link_name_exists(dn_name, payment_type):
# 			continue

# 		# ✅ rate logic
# 		if payment_type == "Labour Payment":
# 			rate = r.get("custom_labour_rate") or 0
# 		else:
# 			rate = amt

# 		result.append({
# 			"name": dn_name,
# 			"party_name": r.get("customer_name"),   # ✅ as requested
# 			"amount": amt,
# 			"payment_type": payment_type,
# 			"date": r.get("posting_date"),          # ✅ as requested
# 			"rate": rate,                           # ✅ as requested
# 		})

# 	return result

import frappe
from frappe.utils import getdate
from mohan_impex.is_created import is_link_name_exists


@frappe.whitelist()
def dn_invoice(party_name=None, payment_type=None, from_date=None, to_date=None):
	party_name = (party_name or "").strip()
	payment_type = (payment_type or "").strip()

	mapping = {
		"Labour Payment": {
			"amount_field": "custom_total_labour_cost",
			"party_field": "contractors_name",
		},
		"Transporter Payment": {
			"amount_field": "custom_transport_charges",
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

	meta = frappe.get_meta("Delivery Note")

	# safety check for dynamic amount field
	if not meta.has_field(amount_field):
		frappe.throw(f"Field '{amount_field}' not found in Delivery Note")

	# fields to fetch (safe)
	fields = ["name", party_field, amount_field]

	has_posting_date = meta.has_field("posting_date")
	if has_posting_date:
		fields.append("posting_date")

	# optional: used for display in child row
	if meta.has_field("customer_name"):
		fields.append("customer_name")

	# rate only for labour
	if meta.has_field("custom_labour_rate"):
		fields.append("custom_labour_rate")

	# qty (for your new child field)
	# Delivery Note has total_qty in standard, but keep safe
	has_total_qty = meta.has_field("total_qty")
	if has_total_qty:
		fields.append("total_qty")

	filters = {"docstatus": 1, amount_field: (">", 0)}

	# party filter if provided
	if party_name:
		filters[party_field] = party_name

	# date filters if provided
	if from_date and to_date and has_posting_date:
		filters["posting_date"] = ["between", [getdate(from_date), getdate(to_date)]]

	order_by = "posting_date desc" if has_posting_date else "modified desc"

	rows = frappe.db.get_all(
		"Delivery Note",
		filters=filters,
		fields=fields,
		order_by=order_by,
	)

	result = []
	for r in rows:
		dn_name = r.get("name")
		amt = r.get(amount_field) or 0

		if amt <= 0:
			continue

		# skip already linked in Purchase Invoice for same service_payment_type
		if is_link_name_exists(dn_name, payment_type):
			continue

		# rate logic
		if payment_type == "Labour Payment":
			rate = r.get("custom_labour_rate") or 0
		else:
			rate = amt

		result.append({
			"name": dn_name,
			"party_name": r.get("customer_name") or "",   # requested
			"amount": amt,
			"payment_type": payment_type,
			"date": r.get("posting_date") if has_posting_date else None,
			"rate": rate,
			"total_qty": r.get("total_qty") if has_total_qty else 0,
		})

	return result



