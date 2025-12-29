import frappe
from mohan_impex.is_created import is_link_name_exists


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
			"amount_field": "transport_charges",   # ✅ CONFIRMED CORRECT
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

	# ✅ Safety check (prevents SQL error)
	if not frappe.get_meta("Purchase Receipt").has_field(amount_field):
		frappe.throw(f"Field '{amount_field}' not found in Purchase Receipt")

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

	result = []
	for r in rows:
		pr_name = r.get("name")
		amt = r.get(amount_field) or 0

		if amt <= 0:
			continue

		# ✅ Skip if already linked in Purchase Invoice for same service_payment_type
		if is_link_name_exists(pr_name, payment_type):
			continue

		result.append({
			"name": pr_name,
			"party_name": r.get(party_field),
			"amount": amt,
			"payment_type": payment_type
		})

	return result
