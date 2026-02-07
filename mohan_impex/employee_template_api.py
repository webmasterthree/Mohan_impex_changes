import frappe
from frappe import _

@frappe.whitelist()
def get_employees_from_template(template_name):
    try:
        template = frappe.get_doc('Employee Template', template_name)
        template.flags.ignore_permissions = True  # Bypass permission check
        template.load_from_db()

        # Extract employee IDs from the child table
        employee_ids = [row.employee for row in template.assign_employee if row.employee]
        return employee_ids

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_employees_from_template")
        frappe.throw(_("Failed to fetch employees from the template."))



