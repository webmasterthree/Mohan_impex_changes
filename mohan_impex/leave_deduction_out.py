# import frappe
# from frappe.utils import nowdate, get_datetime
# from frappe import _
# from datetime import timedelta


# def before_save_employee_checkin(doc, method=None):
#     """
#     Before saving Employee Checkin, check monthly early checkout count (for OUT)
#     and create Leave Application if necessary.
#     """
#     if doc.log_type == "OUT":
#         # Get current month's early checkout count
#         early_checkouts = get_employee_early_checkouts(doc.employee)

#         frappe.logger().info(f"[Monthly] Employee {doc.employee} has {early_checkouts} early check-outs in current month.")

#         # Proceed if early check-outs hit a multiple of 3
#         if early_checkouts % 3 == 0 and early_checkouts > 0:
#             frappe.msgprint(_("Early check-outs reached a multiple of 3 this month. Checking leave availability..."))

#             # Leave types in order of deduction
#             leave_priority = ["Casual Leave", "Sick Leave", "Earned Leave", "Leave Without Pay"]

#             for leave_type in leave_priority:
#                 response = create_leave_application(doc.employee, leave_type)
#                 if "Created" in response:
#                     frappe.msgprint(response)
#                     frappe.logger().info(response)
#                     break
#                 elif "already exists" in response:
#                     frappe.msgprint(response)
#                     break
#             else:
#                 frappe.msgprint(_("No available leave types. Check-out allowed without leave deduction."))


# def get_employee_early_checkouts(employee):
#     """Fetch early check-out count for a specific employee in the current month."""
#     today_date = get_datetime().date()
#     first_day_of_month = today_date.replace(day=1)

#     checkouts = frappe.db.get_all(
#         "Employee Checkin",
#         filters={
#             "log_type": "OUT",
#             "employee": employee,
#             "time": ["between", [first_day_of_month, today_date]]
#         },
#         fields=["shift_end", "time"]
#     )

#     early_count = 0
#     for checkout in checkouts:
#         if not checkout.get("shift_end") or not checkout.get("time"):
#             continue  # Skip incomplete records

#         shift_end = get_datetime(checkout["shift_end"])
#         checkout_time = get_datetime(checkout["time"])

#         # Consider early if left 16 minutes or more before shift end
#         if checkout_time < (shift_end - timedelta(minutes=16)):
#             early_count += 1

#     return early_count


# def get_leave_balances(employee):
#     """Fetch leave balances for a specific employee."""
#     leave_balances = frappe.db.sql(
#         """
#         SELECT leave_type,
#         SUM(CASE WHEN transaction_type = 'Leave Allocation' THEN leaves ELSE 0 END) -
#         SUM(CASE WHEN transaction_type = 'Leave Application' THEN leaves ELSE 0 END) AS leave_balance
#         FROM `tabLeave Ledger Entry`
#         WHERE docstatus = 1 AND employee = %s
#         GROUP BY leave_type
#         """,
#         (employee,),
#         as_dict=True
#     )

#     return {record["leave_type"]: record["leave_balance"] for record in leave_balances}


# @frappe.whitelist()
# def create_leave_application(employee, leave_type):
#     """Creates a Leave Application for the given leave type if available."""
#     leave_balance = get_leave_balances(employee).get(leave_type, 0)

#     if leave_balance <= 0:
#         return f"{leave_type} is not available for Employee {employee}."

#     # Prevent duplicate leave application for today
#     existing_leave = frappe.db.exists("Leave Application", {
#         "employee": employee,
#         "leave_type": leave_type,
#         "from_date": nowdate(),
#         "to_date": nowdate(),
#         "status": ["!=", "Rejected"]
#     })

#     if existing_leave:
#         return f"Leave Application already exists for Employee {employee} today."

#     try:
#         leave_doc = frappe.get_doc({
#             "doctype": "Leave Application",
#             "employee": employee,
#             "leave_type": leave_type,
#             "from_date": nowdate(),
#             "to_date": nowdate(),
#             "posting_date": nowdate(),
#             "description": "Auto Leave Deducted due to Monthly 3x Early Check-Outs",
#             "status": "Approved"
#         })
#         leave_doc.insert(ignore_permissions=True)
#         leave_doc.submit()

#         return f"{leave_type} Leave Application Created for Employee: {employee}."
#     except Exception as e:
#         frappe.logger().error(f"Error creating leave application for {employee}: {str(e)}")
#         return "Failed to create Leave Application. Please check logs."



import frappe
from frappe.utils import (
    getdate, get_first_day, get_last_day,
    time_diff_in_hours, get_datetime
)
from datetime import datetime, time

def after_insert(doc, method):
    emp = frappe.get_doc("Employee",doc.employee)
    if emp.custom_allow_overtime:
        # Only run on OUT
        if doc.log_type != "OUT":
            return

        attendance_date = getdate(doc.time)

        start_datetime = datetime.combine(attendance_date, time.min)
        end_datetime = datetime.combine(attendance_date, time.max)

        # Get IN record of same day
        in_time = frappe.db.get_value(
            "Employee Checkin",
            {
                "employee": doc.employee,
                "log_type": "IN",
                "time": ["between", [start_datetime, end_datetime]],
            },
            "time",
            order_by="time asc"
        )

        if not in_time:
            return

        actual_hours = time_diff_in_hours(doc.time, in_time)

        # Get Shift Type
        if not doc.shift:
            return

        shift = frappe.get_doc("Shift Type", doc.shift)
        shift_hours = time_diff_in_hours(shift.end_time, shift.start_time)

        if actual_hours <= shift_hours:
            return

        overtime_hours = actual_hours - shift_hours

        # Month range
        from_date = get_first_day(attendance_date)
        to_date = get_last_day(attendance_date)

        # Get or create Overtime doc
        overtime_name = frappe.db.get_value(
            "Overtime",
            {
                "employee": doc.employee,
                "from_date": from_date,
                "to_date": to_date,
            }
        )

        if overtime_name:
            overtime = frappe.get_doc("Overtime", overtime_name)
        else:
            overtime = frappe.new_doc("Overtime")
            overtime.employee = doc.employee
            overtime.from_date = from_date
            overtime.to_date = to_date

        # Check if date already exists in child table
        for row in overtime.overtime_table:
            if row.attendance_date == attendance_date:
                row.overtime_hours = overtime_hours
                break
        else:
            overtime.append("overtime_table", {
                "attendance_date": attendance_date,
                "overtime_hours": overtime_hours
            })

        # Update total overtime
        overtime.total_overtime_hours = sum(
            d.overtime_hours for d in overtime.overtime_table
        )

        overtime.save(ignore_permissions=True)
