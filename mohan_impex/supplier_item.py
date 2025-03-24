import frappe
from frappe import _

@frappe.whitelist()
def get_suppliers_by_item(item_name):
    suppliers = frappe.get_all(
        "Item Supplier",
        filters={"parent": item_name},
        pluck="supplier"
    )

    if not suppliers:
        return {"status": "error", "message": _("No suppliers found for this item.")}

    return {"item": item_name, "suppliers": suppliers}


import frappe
import json

@frappe.whitelist()
def get_supplier_portal_users(user_email=None):
    if not user_email:
        user_email = frappe.session.user  # Get the logged-in user

    portal_user = frappe.db.get_all(
        "Portal User",
        filters={"user": user_email, "parenttype": "Supplier"},
        fields=["parent"]  # Fetch only the Supplier name
    )

    if portal_user:
        return [{"supplier": portal_user[0]["parent"]}]  # Return supplier name

    return []
