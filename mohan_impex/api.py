# import frappe
# from frappe.utils import get_datetime, time_diff_in_seconds
# from frappe import _

# @frappe.whitelist()
# def get_employee_late_summary():
#     """Returns a summary of total late check-ins and total late minutes for each employee"""
    
#     if not frappe.has_permission("Employee Checkin", "read"):
#         frappe.throw(_("Not Permitted"), frappe.PermissionError)
    
#     # Fetch Employee Check-ins with shift details
#     checkins = frappe.db.get_all(
#         "Employee Checkin",
#         filters={"log_type": "IN"},
#         fields=["employee", "employee_name", "shift_start", "time"]
#     )

#     late_summary_by_employee = {}

#     for checkin in checkins:
#         if checkin["shift_start"] and checkin["time"]:
#             shift_start = get_datetime(checkin["shift_start"])
#             checkin_time = get_datetime(checkin["time"])

#             # Calculate time difference in seconds
#             time_difference = time_diff_in_seconds(checkin_time, shift_start)

#             # Consider late only if check-in is 15 minutes (900 seconds) or more late
#             if time_difference > 900:
#                 emp_id = checkin["employee"]
#                 emp_name = checkin["employee_name"]
#                 late_minutes = round(time_difference / 60)  # Convert to minutes

#                 if emp_id not in late_summary_by_employee:
#                     late_summary_by_employee[emp_id] = {
#                         "employee_name": emp_name,
#                         "total_late_minutes": 0,
#                         "late_checkin_count": 0
#                     }

#                 # Increment late check-in count
#                 late_summary_by_employee[emp_id]["late_checkin_count"] += 1

#                 # Add late minutes to total
#                 late_summary_by_employee[emp_id]["total_late_minutes"] += late_minutes

#     return {"status": "success", "data": late_summary_by_employee}
