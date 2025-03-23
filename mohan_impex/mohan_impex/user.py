import frappe

@frappe.whitelist()
def update_emp_role_profile(user, role_profile):
    frappe.db.sql(f"update `tabEmployee` set role_profile='{role_profile}' where user_id='{user}'")