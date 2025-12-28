import frappe

@frappe.whitelist()
def dn_invoice(party_name=None, payment_type=None):
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
		"Delivery Note",
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


# @frappe.whitelist()
# def is_dn_invoice_create():
#     invoices = frappe.db.get_all(
#         "Purchase Invoice",
#         fields=["name", "supplier"],
#         filters={
#             "payment_against": ["in", ["Purchase Receipt", "Delivery Note"]]
#         }
#     )

#     result = []

#     for inv in invoices:
#         doc = frappe.get_doc("Purchase Invoice", inv.name)

#         links_data = []
#         for row in doc.links:
#             links_data.append({
#                 "document_type": row.document_type,
#                 "link_name": row.link_name,
#                 "amount": row.amount
#             })

#         result.append({
#             "name": doc.name,
#             "supplier": doc.supplier,
#             "payment_against": doc.payment_against,
#             "links": links_data
#         })

#     return result


import frappe

@frappe.whitelist()
def is_link_name_exists(link_name: str):
    link_name = (link_name or "").strip()
    if not link_name:
        return {"exists": False, "message": "link_name is required"}

    row = frappe.db.sql(
        """
        SELECT lnk.name AS link_row, lnk.parent AS purchase_invoice
        FROM `tabPayment Doc Type` lnk
        INNER JOIN `tabPurchase Invoice` pi ON pi.name = lnk.parent
        WHERE lnk.link_name = %(link_name)s
          AND pi.docstatus != 2
        LIMIT 1
        """,
        {"link_name": link_name},
        as_dict=True
    )

    return {
        "exists": bool(row),
        "purchase_invoice": row[0]["purchase_invoice"] if row else None,
        "link_row": row[0]["link_row"] if row else None
    }
