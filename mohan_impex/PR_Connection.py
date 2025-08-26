# import frappe

# @frappe.whitelist()
# def get_linked_purchase_order(purchase_receipt):
#     """
#     Fetch the linked Purchase Order for a given Purchase Receipt.
#     """
#     try:
#         purchase_order = frappe.db.get_value(
#             "Purchase Receipt Item",
#             {"parent": purchase_receipt},
#             "purchase_order"
#         )

#         return purchase_order if purchase_order else None

#     except Exception as e:
#         frappe.log_error(f"Error fetching linked PO: {str(e)}", "Purchase API Error")
#         return {"status": "error", "message": str(e)}


import frappe

@frappe.whitelist()
def get_linked_purchase_order(purchase_receipt):
    """
    Fetch the linked Purchase Order and custom fields for a given Purchase Receipt.
    """
    try:
        # Get linked Purchase Order name from Purchase Receipt Item
        purchase_order = frappe.db.get_value(
            "Purchase Receipt Item",
            {"parent": purchase_receipt},
            "purchase_order"
        )

        if not purchase_order:
            return None

        # Load Purchase Order doc
        po_doc = frappe.get_doc("Purchase Order", purchase_order)

        # Return selected fields (including your custom ones)
        return {
            "name": po_doc.name,
            "supplier": po_doc.supplier,
            "transaction_date": po_doc.transaction_date,
            "status": po_doc.status,
            # your custom fields 👇
            "custom_transporter_name": po_doc.custom_transporter_name,
            "custom_vehiclecontainer_number": po_doc.custom_vehiclecontainer_number
        }

    except Exception as e:
        frappe.log_error(f"Error fetching linked PO: {str(e)}", "Purchase API Error")
        return {"status": "error", "message": str(e)}
