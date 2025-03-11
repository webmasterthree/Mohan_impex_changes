import frappe

@frappe.whitelist()
def has_supplier_role(user=None):
    if not user:
        user = frappe.session.user

    roles = frappe.get_all("Has Role", filters={"parent": user}, fields=["role"])
    role_names = [r["role"] for r in roles]

    return "Supplier" in role_names
