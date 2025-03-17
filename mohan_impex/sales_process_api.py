import frappe
from frappe import _

@frappe.whitelist()
def get_purchase_order_items(purchase_order=None):
    """Fetch item codes from a specific Purchase Order"""

    try:
        if not purchase_order:
            return {"status": "error", "message": _("Purchase Order is required.")}

        # Fetch only item codes from the given Purchase Order
        items = frappe.db.get_all(
            "Purchase Order Item",
            filters={"parent": purchase_order},
            fields=["item_code"]
        )

        if not items:
            return {"status": "error", "message": _("No items found for this Purchase Order.")}

        return {"status": "success", "data": items}

    except Exception as e:
        return {"status": "error", "message": str(e)}
