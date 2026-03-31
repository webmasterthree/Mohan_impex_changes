import frappe
from frappe.utils import today, get_datetime
from datetime import datetime, timedelta

def monthly_leaves():
    # Define monthly leave allocations per leave type
    monthly_leave_config = {
        "Casual Leave": 0.5,
        "Earned Leave": 1.5,
        "Sick Leave": 0.5
    }

    current_date = get_datetime(today()).date()
    first_day = current_date.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1)  # first day of next month

    employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])

    for emp in employees:
        for leave_type, leave_qty in monthly_leave_config.items():
            existing_allocation = frappe.db.get_value(
                "Leave Allocation", 
                {
                    "employee": emp.name, 
                    "leave_type": leave_type,
                    "from_date": ("<=", first_day),
                    "to_date": (">", first_day)
                }, 
                ["name", "from_date", "to_date", "new_leaves_allocated", "total_leaves_allocated"]
            )

            if existing_allocation:
                existing_name, existing_from, existing_to, existing_new_allocated, existing_total_allocated = existing_allocation

                if isinstance(existing_from, datetime):
                    existing_from = existing_from.date()
                if isinstance(existing_to, datetime):
                    existing_to = existing_to.date()

                new_new_allocated = float(existing_new_allocated or 0) + leave_qty
                new_total_allocated = float(existing_total_allocated or 0) + leave_qty

                frappe.db.set_value("Leave Allocation", existing_name, "new_leaves_allocated", new_new_allocated)
                frappe.db.set_value("Leave Allocation", existing_name, "total_leaves_allocated", new_total_allocated)
                frappe.db.set_value("Leave Allocation", existing_name, "to_date", last_day)

                print(f"Updated {emp.name} - {leave_type}: +{leave_qty} leaves, new total: {new_total_allocated}")
                continue

            # Create new leave allocation
            leave_allocation = frappe.get_doc({
                "doctype": "Leave Allocation",
                "employee": emp.name,
                "leave_type": leave_type,
                "from_date": first_day,
                "to_date": last_day,
                "new_leaves_allocated": leave_qty,
                "total_leaves_allocated": leave_qty,
                "carry_forward": 1
            })
            leave_allocation.insert()
            leave_allocation.submit()

            print(f"Leave allocated: {emp.name} - {leave_type}")

    frappe.msgprint("Monthly Leave Allocation Completed!")
