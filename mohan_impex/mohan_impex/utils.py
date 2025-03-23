import frappe

@frappe.whitelist()
def get_session_employee():
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")
    return emp