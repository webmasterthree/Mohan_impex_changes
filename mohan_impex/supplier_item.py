import frappe
from frappe import _

@frappe.whitelist()
def get_suppliers_by_item(item_name):
    """
    Fetch suppliers linked to a specific item and return only supplier names
    """
    suppliers = frappe.get_all(
        "Item Supplier",  # Child Table
        filters={"parent": item_name},  # Match Item Name
        pluck="supplier"  # This directly returns a list of supplier names
    )

    if not suppliers:
        return {"status": "error", "message": _("No suppliers found for this item.")}

    return {"item": item_name, "suppliers": suppliers}
