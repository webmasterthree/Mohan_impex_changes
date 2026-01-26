import frappe

@frappe.whitelist()
def get_supplier_for_user():
    current_user = frappe.session.user
    result = frappe.db.get_value("Portal User", {"user": current_user}, "parent")
    return result


import frappe

@frappe.whitelist()
def transporter_user():
    current_user = frappe.session.user
    result = frappe.db.get_value("Portal User", {"user": current_user}, "parent")
    return result

import frappe

@frappe.whitelist()
def has_supplier_role(user=None):
    if not user:
        user = frappe.session.user

    roles = frappe.get_all("Has Role", filters={"parent": user}, fields=["role"])
    role_names = [r["role"] for r in roles]

    return "Supplier" in role_names


import frappe
@frappe.whitelist()
def has_transporter_role(user=None):
    if not user:
        user = frappe.session.user

    roles = frappe.get_all("Has Role", filters={"parent": user}, fields=["role"])
    role_names = [r["role"] for r in roles]

    return "MI Transporter" in role_names



import frappe

@frappe.whitelist()
def transporter_name(user_email=None):
    user_email = user_email or frappe.session.user
    transporter = frappe.db.get_value("Portal User", {"user": user_email}, "parent")

    return frappe.db.get_all(
        "Supplier",
        fields=["name", "supplier_name"],
        filters={
            "is_transporter": 1,
            "disabled": 0,
            "name": transporter
        }
    )
