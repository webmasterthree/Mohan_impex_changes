import frappe

@frappe.whitelist()
def get_session_employee():
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name") or ""
    return emp

@frappe.whitelist()
def get_session_emp_role():
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, "role_profile") or ""
    return emp

@frappe.whitelist()
def get_session_employee_area():
    emp_area = frappe.get_value("Employee", {"user_id": frappe.session.user}, "area")
    return emp_area