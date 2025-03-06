import frappe

def get_leave_balances():
    leave_balances = frappe.db.sql("""
        SELECT employee, leave_type,
        SUM(CASE WHEN transaction_type = 'Leave Allocation' THEN leaves ELSE 0 END) -
        SUM(CASE WHEN transaction_type = 'Leave Application' THEN leaves ELSE 0 END) AS leave_balance
        FROM `tabLeave Ledger Entry`
        WHERE docstatus = 1
        GROUP BY employee, leave_type
        ORDER BY employee, leave_type
    """, as_dict=True)

    return leave_balances

# Example usage
balances = get_leave_balances()
for balance in balances:
    print(f"Employee: {balance['employee']}, Leave Type: {balance['leave_type']}, Balance: {balance['leave_balance']}")


import frappe
from frappe.utils import get_datetime
from datetime import timedelta  # Using Python's built-in timedelta

@frappe.whitelist()
def get_employee_late_checkins():
    """
    API to fetch employee-wise late check-in count.
    Returns JSON response with employee ID, employee name, and late check-in count.
    """

    checkins = frappe.db.get_all(
        "Employee Checkin",
        filters={"log_type": "IN"},
        fields=["employee", "employee_name", "shift_start", "time"]
    )

    late_checkin_count = {}

    for checkin in checkins:
        shift_start = get_datetime(checkin["shift_start"])
        checkin_time = get_datetime(checkin["time"])

        # Check if check-in time is more than 15 minutes after shift start
        if checkin_time > (shift_start + timedelta(minutes=15)):  # Fixed without add_minutes
            employee = checkin["employee"]
            if employee in late_checkin_count:
                late_checkin_count[employee]["late_count"] += 1
            else:
                late_checkin_count[employee] = {
                    "employee_name": checkin["employee_name"],
                    "late_count": 1
                }

    return list(late_checkin_count.values())  # Returns JSON response
