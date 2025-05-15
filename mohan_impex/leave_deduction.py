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
