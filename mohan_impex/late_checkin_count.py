import frappe
from frappe.utils import get_time
from frappe import _

@frappe.whitelist()
def get_employee_late_checkins():
    """
    Returns a list of dictionaries with employee-wise late check-in counts.
    Also updates each Employee's 'custom_late_checkin_count' field.
    Only updates employees with at least one late check-in.
    """
    late_checkins_by_employee = {}

    checkins = frappe.db.get_all(
        'Employee Checkin',
        fields=["employee", "employee_name", "shift_start", "time", "log_type"],
        filters={"log_type": "IN"}
    )

    for c in checkins:
        if c.shift_start and c.time:
            if get_time(c.time) > get_time(c.shift_start):
                if c.employee not in late_checkins_by_employee:
                    late_checkins_by_employee[c.employee] = {
                        "employee": c.employee,
                        "employee_name": c.employee_name,
                        "late_checkins": 1
                    }
                else:
                    late_checkins_by_employee[c.employee]["late_checkins"] += 1

    # Update only employees with late check-ins
    for emp, data in late_checkins_by_employee.items():
        frappe.db.set_value("Employee", emp, "custom_late_checkin_count", data["late_checkins"])
    frappe.db.commit()
    return list(late_checkins_by_employee.values())


# import frappe
# from frappe.utils import get_time
# from collections import defaultdict
# from frappe import _

# @frappe.whitelist()
# def get_employee_late_checkins():
#     """
#     Returns a list of dictionaries with employee-wise late check-in counts.
#     """
#     late_checkins_by_employee = {}

#     checkins = frappe.db.get_all(
#         'Employee Checkin',
#         fields=["employee", "employee_name", "shift_start", "time", "log_type"],
#         filters={"log_type": "IN"}
#     )

#     for c in checkins:
#         if c.shift_start and c.time:
#             if get_time(c.time) > get_time(c.shift_start):
#                 if c.employee not in late_checkins_by_employee:
#                     late_checkins_by_employee[c.employee] = {
#                         "employee": c.employee,
#                         "employee_name": c.employee_name,
#                         "late_checkins": 1
#                     }
#                 else:
#                     late_checkins_by_employee[c.employee]["late_checkins"] += 1

#     # Return as list
#     return list(late_checkins_by_employee.values())
