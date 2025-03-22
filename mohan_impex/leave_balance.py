import frappe
from frappe.utils import today, get_datetime
from datetime import datetime, timedelta

def allocate_monthly_leave():
    # Define monthly leave allocations per leave type
    monthly_leave_config = {
        "Casual Leave": 0.5,
        "Earned Leave": 1.5,
        "Sick Leave": 0.5
    }

    current_date = get_datetime(today()).date()
    first_day = current_date.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])

    for emp in employees:
        for leave_type, leave_qty in monthly_leave_config.items():
            existing_allocation = frappe.db.get_value(
                "Leave Allocation", 
                {"employee": emp.name, "leave_type": leave_type}, 
                ["name", "from_date", "to_date", "total_leaves_allocated"]
            )

            if existing_allocation:
                existing_name, existing_from, existing_to, allocated_leaves = existing_allocation

                if isinstance(existing_from, datetime):
                    existing_from = existing_from.date()
                if isinstance(existing_to, datetime):
                    existing_to = existing_to.date()

                if existing_from <= first_day <= existing_to:
                    print(f"Skipping {emp.name} - {leave_type} (Already allocated: {allocated_leaves} in {existing_name})")
                    continue

                # Update existing allocation (extend the period and increment leave count)
                print(f"Updating allocation for {emp.name} - {leave_type}")
                frappe.db.set_value("Leave Allocation", existing_name, "to_date", last_day)
                frappe.db.set_value("Leave Allocation", existing_name, "total_leaves_allocated", allocated_leaves + leave_qty)
                continue

            # Create new leave allocation
            leave_allocation = frappe.get_doc({
                "doctype": "Leave Allocation",
                "employee": emp.name,
                "leave_type": leave_type,
                "from_date": first_day,
                "to_date": last_day,
                "new_leaves_allocated": leave_qty,
                "carry_forward": 1
            })
            leave_allocation.insert()
            leave_allocation.submit()

            print(f"Leave allocated: {emp.name} - {leave_type}")

    frappe.msgprint("Monthly Leave Allocation Completed!")

# import frappe
# import json

# def get_all_leave_balances():
#     leave_entries = frappe.db.get_all(
#         "Leave Ledger Entry",
#         fields=["employee", "employee_name", "leave_type", "leaves"]
#     )

#     leave_balances = {}

#     for entry in leave_entries:
#         employee_key = f"{entry['employee']} ({entry['employee_name']})"

#         if employee_key not in leave_balances:
#             leave_balances[employee_key] = {}

#         leave_type = entry["leave_type"]
#         if leave_type not in leave_balances[employee_key]:
#             leave_balances[employee_key][leave_type] = 0
        
#         leave_balances[employee_key][leave_type] += entry["leaves"]

#     # Convert to JSON format and print
#     print(json.dumps(leave_balances, indent=4))

# get_all_leave_balances()



# import frappe
# from frappe.utils import today, get_datetime
# from datetime import datetime, timedelta

# def allocate_monthly_leaves():
#     employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name"])

#     for emp in employees:
#         # Fetch leave types that should be allocated monthly
#         leave_types = frappe.get_all("Leave Type", filters={"is_lwp": 0}, fields=["name"])

#         for leave in leave_types:
#             # Get first and last day of the current month manually
#             current_date = get_datetime(today()).date()  # Convert to date
#             first_day = current_date.replace(day=1)  # First day of the month
#             last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Last day of the month

#             # Check if any overlapping leave allocation exists
#             existing_allocation = frappe.db.get_value(
#                 "Leave Allocation", 
#                 {"employee": emp.name, "leave_type": leave.name}, 
#                 ["name", "from_date", "to_date", "total_leaves_allocated"]
#             )

#             if existing_allocation:
#                 existing_name, existing_from, existing_to, allocated_leaves = existing_allocation

#                 # Convert `first_day` and `last_day` to date type
#                 if isinstance(existing_from, datetime):
#                     existing_from = existing_from.date()
#                 if isinstance(existing_to, datetime):
#                     existing_to = existing_to.date()

#                 # If the existing allocation covers this month, skip
#                 if existing_from <= first_day <= existing_to:
#                     print(f"Skipping {emp.name} - {leave.name} (Already allocated: {allocated_leaves} leaves in {existing_name})")
#                     continue

#                 # If the allocation exists but is for a different period, extend it
#                 print(f"Updating existing allocation for {emp.name} - {leave.name}")
#                 frappe.db.set_value("Leave Allocation", existing_name, "to_date", last_day)
#                 frappe.db.set_value("Leave Allocation", existing_name, "total_leaves_allocated", allocated_leaves + 1)
#                 continue

#             # Create new leave allocation
#             leave_allocation = frappe.get_doc({
#                 "doctype": "Leave Allocation",
#                 "employee": emp.name,
#                 "leave_type": leave.name,
#                 "from_date": first_day,
#                 "to_date": last_day,
#                 "new_leaves_allocated": 1  # Assign 1 leave per month
#             })
#             leave_allocation.insert()
#             leave_allocation.submit()

#             # Print message for debugging
#             print(f"Leave allocated: {emp.name} - {leave.name}")

#     frappe.msgprint("Monthly Leave Allocation Completed!")
