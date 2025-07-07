import frappe
from frappe import _

@frappe.whitelist()
def get_employees_from_template(template_name):
    try:
        # Load the Employee Template
        template = frappe.get_doc('Employee Template', template_name)

        # Extract unique employee IDs from child table
        employee_ids = {
            row.employee
            for row in template.assign_employee
            if row.employee
        }

        return list(employee_ids)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_employees_from_template")
        frappe.throw(_("Something went wrong while retrieving employees."))

# import frappe
# from frappe import _

# @frappe.whitelist()
# def get_employees_from_template(template_name):
#     if not frappe.has_permission("Employee Template", "read"):
#         frappe.throw(_("Not permitted"), frappe.PermissionError)

#     try:
#         # Load the Employee Template
#         template = frappe.get_doc('Employee Template', template_name)

#         # Extract unique employee IDs from child table
#         employee_ids = {
#             row.employee
#             for row in template.assign_employee
#             if row.employee
#         }

#         return list(employee_ids)

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Error in get_employees_from_template")
#         frappe.throw(_("Something went wrong while retrieving employees."))
