# import frappe

# @frappe.whitelist()
# def pr_invoice(party_name=None, payment_type=None):
#     party_name = (party_name or "").strip()
#     payment_type = (payment_type or "").strip()

#     mapping = {
#         "Labour Payment": {
#             "amount_field": "custom_total_labour_cost",
#             "party_field": "contractors_name"
#         },
#         "Transporter Payment": {
#             "amount_field": "transport_charges",
#             "party_field": "transporter"
#         },
#         "Miscellaneous Payment": {
#             "amount_field": "total_misc_amount",
#             "party_field": "misc_supplier"
#         }
#     }

#     if payment_type not in mapping:
#         frappe.throw("Invalid payment_type")

#     amount_field = mapping[payment_type]["amount_field"]
#     party_field = mapping[payment_type]["party_field"]

#     filters = {
#         "docstatus": 1,
#         amount_field: (">", 0)
#     }

#     # Apply party filter if provided
#     if party_name:
#         filters[party_field] = party_name

#     invoices = frappe.db.get_all(
#         "Purchase Receipt",
#         filters=filters,
#         fields=["name", party_field, amount_field]
#     )

#     result = []

#     for inv in invoices:
#         cleaned = {
#             k: v for k, v in inv.items()
#             if v not in (None, 0, 0.0)
#         }
#         result.append(cleaned)

#     return result


import frappe

@frappe.whitelist()
def pr_invoice(party_name=None, payment_type=None):
	party_name = (party_name or "").strip()
	payment_type = (payment_type or "").strip()

	mapping = {
		"Labour Payment": {
			"amount_field": "custom_total_labour_cost",
			"party_field": "contractors_name"
		},
		"Transporter Payment": {
			"amount_field": "transport_charges",
			"party_field": "transporter"
		},
		"Miscellaneous Payment": {
			"amount_field": "total_misc_amount",
			"party_field": "misc_supplier"
		}
	}

	if payment_type not in mapping:
		frappe.throw("Invalid payment_type")

	amount_field = mapping[payment_type]["amount_field"]
	party_field = mapping[payment_type]["party_field"]

	filters = {"docstatus": 1, amount_field: (">", 0)}

	# party filter if provided
	if party_name:
		filters[party_field] = party_name

	rows = frappe.db.get_all(
		"Purchase Receipt",
		filters=filters,
		fields=["name", party_field, amount_field],
		order_by="posting_date desc"
	)

	# ✅ Standard output keys: name, party_name, amount
	result = []
	for r in rows:
		amt = r.get(amount_field) or 0
		if amt > 0:
			result.append({
				"name": r.get("name"),
				"party_name": r.get(party_field),
				"amount": amt,
				"payment_type": payment_type
			})

	return result
