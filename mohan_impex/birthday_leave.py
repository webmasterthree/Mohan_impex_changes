import frappe
from frappe.utils import nowdate, getdate

def send_birthday_notification():
    today = getdate(nowdate())
    current_month = today.month
    current_year = today.year

    employees = frappe.db.get_all(
        'Employee',
        fields=["employee", "employee_name", "user_id", "date_of_birth"],
        filters={"status": "Active"}
    )

    for emp in employees:
        dob = getdate(emp.date_of_birth) if emp.date_of_birth else None

        if dob and dob.month == current_month and emp.user_id:
            user_id = emp.user_id

            # Check if Casual Leave is already applied this month
            has_leave = frappe.db.exists(
                "Leave Application",
                {
                    "employee": emp.employee,
                    "leave_type": "Birthday Month Leave",
                    "from_date": (">=", f"{current_year}-{current_month:02d}-01"),
                    "to_date": ("<=", f"{current_year}-{current_month:02d}-31"),
                    "docstatus": 1  # Approved
                }
            )

            if has_leave:
                continue  # Skip if already applied for CL this month

            try:
                frappe.get_doc({
                    "doctype": "PWA Notification",
                    "to_user": user_id,
                    "from_user": "Administrator",
                    "reference_document_type": "Leave Application",
                    "reference_document_name": emp.employee,
                    "message": (
                        f"🎉 {emp.employee_name}, your birthday is this month! "
                        f"Don't forget to take your Birthday Leave — it'll expire soon if unused!"
                    )
                }).insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(
                    title="Birthday Month Notification Error",
                    message=f"Failed to create birthday/leave notification for {emp.employee_name} ({user_id}): {str(e)}"
                )

# import frappe
# from frappe.utils import nowdate, getdate

# @frappe.whitelist()
# def get_birthdays_this_month():
#     current_month = getdate(nowdate()).month

#     employees = frappe.db.get_all(
#         'Employee',
#         fields=["employee", "employee_name", "user_id", "date_of_birth"],
#         filters={
#             "status": "Active"
#         }
#     )

#     result = [
#         emp for emp in employees
#         if emp.date_of_birth and getdate(emp.date_of_birth).month == current_month
#     ]

#     return result
