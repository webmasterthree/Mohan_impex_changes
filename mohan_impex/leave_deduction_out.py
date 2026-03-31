import frappe
from frappe.utils import nowdate, get_datetime
from frappe import _
from datetime import timedelta


def before_save_employee_checkin(doc, method):
    """
    Before saving Employee Checkin, check monthly early checkout count (for OUT)
    and create Leave Application if necessary.
    """
    if doc.log_type == "OUT":
        # Get current month's early checkout count
        early_checkouts = get_employee_early_checkouts(doc.employee)

        frappe.logger().info(f"[Monthly] Employee {doc.employee} has {early_checkouts} early check-outs in current month.")

        # Proceed if early check-outs hit a multiple of 3
        if early_checkouts % 3 == 0 and early_checkouts > 0:
            frappe.msgprint(_("Early check-outs reached a multiple of 3 this month. Checking leave availability..."))

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
                frappe.msgprint(_("No available leave types. Check-out allowed without leave deduction."))


def get_employee_early_checkouts(employee):
    """Fetch early check-out count for a specific employee in the current month."""
    today_date = get_datetime().date()
    first_day_of_month = today_date.replace(day=1)

    checkouts = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "log_type": "OUT",
            "employee": employee,
            "time": ["between", [first_day_of_month, today_date]]
        },
        fields=["shift_end", "time"]
    )

    early_count = 0
    for checkout in checkouts:
        if not checkout.get("shift_end") or not checkout.get("time"):
            continue  # Skip incomplete records

        shift_end = get_datetime(checkout["shift_end"])
        checkout_time = get_datetime(checkout["time"])

        # Consider early if left 16 minutes or more before shift end
        if checkout_time < (shift_end - timedelta(minutes=16)):
            early_count += 1

    return early_count


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
            "description": "Auto Leave Deducted due to Monthly 3x Early Check-Outs",
            "status": "Open"
        })
        leave_doc.insert(ignore_permissions=True)
        leave_doc.submit()

        return f"{leave_type} Leave Application Created for Employee: {employee}."
    except Exception as e:
        frappe.logger().error(f"Error creating leave application for {employee}: {str(e)}")
        return "Failed to create Leave Application. Please check logs."
