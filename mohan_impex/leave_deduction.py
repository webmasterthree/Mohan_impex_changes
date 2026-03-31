import frappe
from frappe.utils import nowdate, get_datetime, today
from frappe import _
from datetime import timedelta


def before_save_employee_checkin(doc, method):
    """Before saving Employee Checkin, check monthly late count and create Leave Application if necessary."""
    if doc.log_type == "IN":
        # Get current month's late check-in count
        late_checkins = get_employee_late_checkins(doc.employee)

        frappe.logger().info(f"[Monthly] Employee {doc.employee} has {late_checkins} late check-ins in current month.")

        # Proceed if late check-ins hit a multiple of 3
        if late_checkins % 3 == 0 and late_checkins > 0:
            frappe.msgprint(_("Late check-ins reached a multiple of 3 this month. Checking leave availability..."))

            # Leave types in order of deduction
            leave_priority = ["Casual Leave", "Sick Leave", "Earned Leave", "Leave Without Pay"]

            for leave_type in leave_priority:
                response = create_leave_application(doc.employee, leave_type)
                if "Created" in response:
                    frappe.msgprint(response)
                    frappe.logger().info(response)
                    break
                elif "already exists" in response:
                    frappe.msgprint(response)
                    break
            else:
                frappe.msgprint(_("No available leave types. Check-in allowed without leave deduction."))


def get_employee_late_checkins(employee):
    """Fetch late check-in count for a specific employee in the current month."""
    today_date = get_datetime().date()
    first_day_of_month = today_date.replace(day=1)

    checkins = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "log_type": "IN",
            "employee": employee,
            "time": ["between", [first_day_of_month, today_date]]
        },
        fields=["shift_start", "time"]
    )

    late_count = 0
    for checkin in checkins:
        if not checkin.get("shift_start") or not checkin.get("time"):
            continue  # Skip incomplete records

        shift_start = get_datetime(checkin["shift_start"])
        checkin_time = get_datetime(checkin["time"])

        # Consider late if beyond 16 minutes from shift start
        if checkin_time > (shift_start + timedelta(minutes=16)):
            late_count += 1

    return late_count


def get_leave_balances(employee):
    """Fetch leave balances for a specific employee."""
    leave_balances = frappe.db.sql(
        """
        SELECT leave_type,
        SUM(CASE WHEN transaction_type = 'Leave Allocation' THEN leaves ELSE 0 END) -
        SUM(CASE WHEN transaction_type = 'Leave Application' THEN leaves ELSE 0 END) AS leave_balance
        FROM `tabLeave Ledger Entry`
        WHERE docstatus = 1 AND employee = %s
        GROUP BY leave_type
        """,
        (employee,),
        as_dict=True
    )

    return {record["leave_type"]: record["leave_balance"] for record in leave_balances}


@frappe.whitelist()
def create_leave_application(employee, leave_type):
    """Creates a Leave Application for the given leave type if available."""
    leave_balance = get_leave_balances(employee).get(leave_type, 0)

    if leave_balance <= 0:
        return f"{leave_type} is not available for Employee {employee}."

    # Prevent duplicate leave application for today
    existing_leave = frappe.db.exists("Leave Application", {
        "employee": employee,
        "leave_type": leave_type,
        "from_date": nowdate(),
        "to_date": nowdate(),
        "status": ["!=", "Rejected"]
    })

    if existing_leave:
        return f"Leave Application already exists for Employee {employee} today."

    try:
        leave_doc = frappe.get_doc({
            "doctype": "Leave Application",
            "employee": employee,
            "leave_type": leave_type,
            "from_date": nowdate(),
            "to_date": nowdate(),
            "posting_date": nowdate(),
            "description": "Auto Leave Deducted due to Monthly 3x Late Check-Ins",
            "status": "Open"
        })
        leave_doc.insert(ignore_permissions=True)
        leave_doc.submit()

        return f"{leave_type} Leave Application Created for Employee: {employee}."
    except Exception as e:
        frappe.logger().error(f"Error creating leave application for {employee}: {str(e)}")
        return "Failed to create Leave Application. Please check logs."


#===========#

# import frappe
# from frappe.utils import nowdate, get_datetime, today
# from frappe import _
# from datetime import timedelta


# def before_save_employee_checkin(doc, method):
#     """Before saving Employee Checkin, check monthly late count and create Leave Application if necessary."""
#     if getattr(doc, "log_type", None) != "IN":
#         return

#     # Determine if THIS check-in is late (16-min grace)
#     is_current_late = False
#     try:
#         if getattr(doc, "shift_start", None) and getattr(doc, "time", None):
#             shift_start_dt = get_datetime(doc.shift_start)
#             time_dt = get_datetime(doc.time)
#             is_current_late = time_dt > (shift_start_dt + timedelta(minutes=16))
#     except Exception:
#         is_current_late = False

#     # Count late check-ins for the month from saved rows
#     previous_late = get_employee_late_checkins(doc.employee)

#     # Only proceed if THIS check-in is actually late
#     if not is_current_late:
#         return

#     # Include current late in the tally
#     late_checkins = previous_late + 1

#     frappe.logger().info(f"[Monthly] Employee {doc.employee} has {late_checkins} late check-ins in current month (including current).")

#     # Trigger only when the new tally hits a multiple of 3
#     if late_checkins % 3 == 0:
#         frappe.msgprint(_("Late check-ins reached a multiple of 3 this month. Checking leave availability..."))

#         # Guardrail: if any leave (of any type) already exists for today, skip
#         if frappe.db.exists(
#             "Leave Application",
#             {
#                 "employee": doc.employee,
#                 "from_date": nowdate(),
#                 "to_date": nowdate(),
#                 "status": ["!=", "Rejected"],
#             },
#         ):
#             frappe.msgprint(_("A Leave Application already exists for today. No further deduction."))
#             frappe.logger().info(f"[AutoLeave] Leave already exists today for {doc.employee}; skipping.")
#             return

#         # Figure out which time (1st, 2nd, 3rd...) this is
#         deduction_number = late_checkins // 3
#         ordinal_map = {1: "1st", 2: "2nd", 3: "3rd"}
#         ordinal_suffix = ordinal_map.get(deduction_number, f"{deduction_number}th")

#         # Late milestone: 3, 6, 9, 12, ...
#         late_milestone = deduction_number * 3

#         # Leave types in order of deduction
#         leave_priority = ["Casual Leave", "Sick Leave", "Earned Leave", "Leave Without Pay"]

#         for leave_type in leave_priority:
#             response = create_leave_application(doc.employee, leave_type, ordinal_suffix, late_milestone)
#             frappe.msgprint(response)
#             frappe.logger().info(response)

#             # Stop after the first success OR if one already exists (safety)
#             if "Created" in response or "already exists" in response:
#                 break


# def get_employee_late_checkins(employee):
#     """Fetch late check-in count for a specific employee in the current month."""
#     today_date = get_datetime().date()
#     first_day_of_month = today_date.replace(day=1)

#     checkins = frappe.db.get_all(
#         "Employee Checkin",
#         filters={
#             "log_type": "IN",
#             "employee": employee,
#             "time": ["between", [first_day_of_month, today_date]]
#         },
#         fields=["shift_start", "time"]
#     )

#     late_count = 0
#     for checkin in checkins:
#         if not checkin.get("shift_start") or not checkin.get("time"):
#             continue  # Skip incomplete records

#         shift_start = get_datetime(checkin["shift_start"])
#         checkin_time = get_datetime(checkin["time"])

#         # Consider late if beyond 16 minutes from shift start
#         if checkin_time > (shift_start + timedelta(minutes=16)):
#             late_count += 1

#     return late_count


# def get_leave_balances(employee):
#     """Fetch leave balances for a specific employee (net of ledger entries)."""
#     leave_balances = frappe.db.sql(
#         """
#         SELECT leave_type,
#                COALESCE(SUM(leaves), 0) AS leave_balance
#         FROM `tabLeave Ledger Entry`
#         WHERE docstatus = 1
#           AND employee = %s
#         GROUP BY leave_type
#         """,
#         (employee,),
#         as_dict=True
#     )

#     return {record["leave_type"]: float(record["leave_balance"]) for record in leave_balances}


# @frappe.whitelist()
# def create_leave_application(employee, leave_type, ordinal_suffix=None, late_milestone=None):
#     """Creates a Leave Application for the given leave type if available."""
#     # Block any duplicate leave for today regardless of type
#     existing_any_leave = frappe.db.exists(
#         "Leave Application",
#         {
#             "employee": employee,
#             "from_date": nowdate(),
#             "to_date": nowdate(),
#             "status": ["!=", "Rejected"]
#         }
#     )
#     if existing_any_leave:
#         return f"Leave Application already exists for Employee {employee} today."

#     leave_balance = get_leave_balances(employee).get(leave_type, 0)

#     # For paid leaves, ensure positive balance; allow LWP regardless of balance
#     if leave_type != "Leave Without Pay" and leave_balance <= 0:
#         return f"{leave_type} is not available for Employee {employee}."

#     # Prepare description with ordinal + milestone (e.g. 1st -> 3rd, 2nd -> 6th)
#     if ordinal_suffix and late_milestone:
#         description = f"{ordinal_suffix} Auto Leave Deducted due to Monthly {late_milestone}th Late Check-Ins"
#     else:
#         description = "Auto Leave Deducted due to Monthly 3x Late Check-Ins"

#     try:
#         leave_doc = frappe.get_doc({
#             "doctype": "Leave Application",
#             "employee": employee,
#             "leave_type": leave_type,
#             "from_date": nowdate(),
#             "to_date": nowdate(),
#             "posting_date": nowdate(),
#             "description": description,
#             "status": "Open"
#         })
#         leave_doc.insert(ignore_permissions=True)
#         leave_doc.submit()

#         return f"{leave_type} Leave Application Created for Employee: {employee}."
#     except Exception as e:
#         frappe.logger().error(f"Error creating leave application for {employee}: {str(e)}")
#         return "Failed to create Leave Application. Please check logs."
