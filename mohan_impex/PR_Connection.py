import frappe

@frappe.whitelist()
def get_linked_purchase_order(purchase_receipt):
    """
    Fetch the linked Purchase Order for a given Purchase Receipt.
    """
    try:
        purchase_order = frappe.db.get_value(
            "Purchase Receipt Item",
            {"parent": purchase_receipt},
            "purchase_order"
        )

        return purchase_order if purchase_order else None

    except Exception as e:
        frappe.log_error(f"Error fetching linked PO: {str(e)}", "Purchase API Error")
        return {"status": "error", "message": str(e)}
