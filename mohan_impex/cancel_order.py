import frappe
from frappe.model.document import Document

@frappe.whitelist()
def cancel_sales_order(name, reason):
    try:
        # Get the Sales Order document
        sales_order = frappe.get_doc("Sales Order", name)

        # Check if already cancelled
        if sales_order.docstatus == 2:
            return {"status": "error", "message": "This Sales Order is already cancelled."}

        # Allow modifying the reason before cancelling
        frappe.db.set_value("Sales Order", name, "custom__cancellation_reason", reason, update_modified=True)

        # Reload the document to reflect changes
        sales_order.reload()

        # Cancel the Sales Order
        sales_order.cancel()

        return {"status": "success", "message": f"Sales Order {name} cancelled successfully."}

    except Exception as e:
        frappe.log_error(f"Error cancelling Sales Order {name}: {str(e)}")
        return {"status": "error", "message": str(e)}
