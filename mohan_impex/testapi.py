import frappe

@frappe.whitelist()
def get_employee_leave_balance(employee):
    """
    Returns the net leave balance of all leave types for a given employee.

    Example Output:
    {
        "Sick Leave": 5.5,
        "Earned Leave": 18.0
    }
    """
    if not employee:
        frappe.throw("Employee ID is required")

    # Fetch all leave ledger entries for the employee
    entries = frappe.db.get_all(
        'Leave Ledger Entry',
        filters={'employee': employee},
        fields=['leave_type', 'leaves']
    )

    leave_balance = {}

    for entry in entries:
        leave_type = entry['leave_type']
        leaves = entry['leaves']

        if leave_type not in leave_balance:
            leave_balance[leave_type] = 0.0

        leave_balance[leave_type] += leaves

    return leave_balance
