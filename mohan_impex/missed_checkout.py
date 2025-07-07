import frappe
from frappe import _

@frappe.whitelist()
def get_employee_holidays(employee_id):
    """
    API: Get holiday dates for an employee based on assigned holiday list.
    """
    if not employee_id:
        return {"error": "Employee ID is required."}

    employee = frappe.db.get_value("Employee", employee_id, ["employee_name", "holiday_list"], as_dict=True)

    if not employee:
        return {"error": "Employee not found."}

    if not employee.holiday_list:
        return {"error": f"No holiday list assigned to Employee {employee_id}."}

    holidays = frappe.db.get_all(
        "Holiday",
        filters={"parent": employee.holiday_list},
        fields=["holiday_date", "description"],
        order_by="holiday_date"
    )

    return {
        "employee": employee_id,
        "employee_name": employee.employee_name,
        "holiday_list": employee.holiday_list,
        "holidays": holidays
    }



# import frappe
# from collections import defaultdict
# from datetime import datetime

# @frappe.whitelist()
# def get_today_missed_checkout_status():
#     today = frappe.utils.today()
    
#     # Get all checkins for today
#     checkins = frappe.db.get_all(
#         'Employee Checkin',
#         fields=["employee", "log_type", "time"],
#         filters={
#             "time": ["between", [today + " 00:00:00", today + " 23:59:59"]]
#         },
#         order_by="employee, time"
#     )

#     # Track IN/OUT status per employee
#     status_map = defaultdict(lambda: {"IN": False, "OUT": False})

#     for entry in checkins:
#         emp = entry['employee']
#         status_map[emp][entry['log_type']] = True

#     # Final output: employee -> True (missed) / False (not missed)
#     result = {
#         emp: (status["IN"] and not status["OUT"])
#         for emp, status in status_map.items()
#     }

#     return result


# import frappe
# from collections import defaultdict
# from datetime import datetime

# @frappe.whitelist()
# def get_today_missed_checkout_status():
#     today = frappe.utils.today()
    
#     # Get all checkins for today
#     checkins = frappe.db.get_all(
#         'Employee Checkin',
#         fields=["employee", "log_type", "time"],
#         filters={
#             "time": ["between", [today + " 00:00:00", today + " 23:59:59"]]
#         },
#         order_by="employee, time"
#     )

#     # Track IN/OUT status per employee
#     status_map = defaultdict(lambda: {"IN": False, "OUT": False})

#     for entry in checkins:
#         emp = entry['employee']
#         status_map[emp][entry['log_type']] = True

#     # Final output: employee -> True (missed) / False (not missed)
#     result = {
#         emp: (status["IN"] and not status["OUT"])
#         for emp, status in status_map.items()
#     }

#     return result


# import frappe
# from collections import defaultdict

# @frappe.whitelist()
# def get_today_missed_checkout_status():
#     today = frappe.utils.today()

#     # Step 1: Fetch all checkins for today
#     checkins = frappe.db.get_all(
#         'Employee Checkin',
#         fields=["name", "employee", "employee_name", "log_type", "time"],
#         filters={
#             "time": ["between", [today + " 00:00:00", today + " 23:59:59"]]
#         },
#         order_by="employee, time"
#     )

#     # Step 2: Get user_id for all employees involved
#     employee_ids = list(set([entry['employee'] for entry in checkins]))
#     user_map = {
#         emp['employee']: emp['user_id']
#         for emp in frappe.db.get_all(
#             'Employee',
#             filters={"employee": ["in", employee_ids]},
#             fields=["employee", "user_id"]
#         )
#     }

#     # Step 3: Track IN/OUT and first IN docname
#     status_map = defaultdict(lambda: {
#         "employee_name": "",
#         "name": "",
#         "IN": False,
#         "OUT": False
#     })

#     for entry in checkins:
#         emp = entry['employee']
#         status = status_map[emp]
#         status["employee_name"] = entry["employee_name"]

#         if entry['log_type'] == 'IN':
#             if not status["IN"]:
#                 status["name"] = entry["name"]
#             status["IN"] = True
#         elif entry['log_type'] == 'OUT':
#             status["OUT"] = True

#     # Step 4: Build final result
#     result = []
#     for emp, status in status_map.items():
#         result.append({
#             "name": status["name"],               # Checkin Docname
#             "employee": emp,
#             "employee_name": status["employee_name"],
#             "user_id": user_map.get(emp, ""),     # from Employee
#             "missed_checkout": status["IN"] and not status["OUT"]
#         })

#     return result


import frappe
from collections import defaultdict
from frappe.utils import today

@frappe.whitelist()
def get_today_missed_checkout_statuss():
    current_date = today()

    # Step 1: Get all check-ins for today
    checkins = frappe.db.get_all(
        'Employee Checkin',
        fields=["name", "employee", "employee_name", "log_type", "time"],
        filters={
            "time": ["between", [f"{current_date} 00:00:00", f"{current_date} 23:59:59"]]
        },
        order_by="employee, time"
    )

    if not checkins:
        return []

    # Step 2: Fetch user_id for each employee with valid user_id
    employee_ids = list(set(entry['employee'] for entry in checkins))
    user_map = {
        emp['employee']: emp['user_id']
        for emp in frappe.db.get_all(
            'Employee',
            filters={
                "employee": ["in", employee_ids],
                "user_id": ["!=", ""]
            },
            fields=["employee", "user_id"]
        )
    }

    # Step 3: Determine IN and OUT status for each employee
    status_map = defaultdict(lambda: {
        "employee_name": "",
        "name": "",
        "IN": False,
        "OUT": False
    })

    for entry in checkins:
        emp = entry['employee']
        status = status_map[emp]
        status["employee_name"] = entry["employee_name"]

        if entry['log_type'] == 'IN':
            if not status["IN"]:
                status["name"] = entry["name"]  # Store the first IN checkin name
            status["IN"] = True
        elif entry['log_type'] == 'OUT':
            status["OUT"] = True

    # Step 4: Prepare result and create PWA Notification if checkout is missed
    result = []

    for emp, status in status_map.items():
        missed_checkout = status["IN"] and not status["OUT"]
        user_id = user_map.get(emp)

        result.append({
            "name": status["name"],
            "employee": emp,
            "employee_name": status["employee_name"],
            "user_id": user_id,
            "missed_checkout": missed_checkout
        })

        if missed_checkout:
            if not user_id:
                frappe.logger().info(f"[Missed Checkout] user_id missing for employee: {emp}")
                continue

            try:
                frappe.get_doc({
                    "doctype": "PWA Notification",
                    "to_user": user_id,
                    "from_user": "Administrator",
                    "reference_document_type": "Leave Application",
                    "reference_document_name": status["name"],
                    "message": "One day of your Casual Leave (CL) will be deducted if you continue to miss checkout for three consecutive days."
                }).insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(
                    title="Missed Checkout Notification Error",
                    message=f"Failed to create notification for {emp} ({user_id}): {str(e)}"
                )

    return result
