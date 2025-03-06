# import frappe
# from frappe.utils import getdate
# from mohan_impex.mohan_impex.report.daily_attendance_report import get_employee_attendance_report

# def execute(filters=None):
#     """
#     Generates a Daily Attendance Report including employee details, IN/OUT times, shifts, and attendance status with colored text.
    
#     :param filters: Dictionary containing filter options, e.g., {'date': 'YYYY-MM-DD'}
#     :return: Tuple (columns, data) formatted for ERPNext report generation.
#     """

#     # Default date if not provided
#     date = filters.get("date") if filters else getdate()

#     # Fetch attendance data
#     attendance_data = get_employee_attendance_report(date)
    
#     if attendance_data.get("status") != "success":
#         frappe.throw("Error fetching attendance data: " + attendance_data.get("message", "Unknown error"))

#     # Define report columns with Status color formatting
#     columns = [
#         {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
#         {"fieldname": "employee", "label": "Employee ID", "fieldtype": "Data", "width": 120},
#         {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
#         {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 150},
#         {"fieldname": "shift", "label": "Shift", "fieldtype": "Data", "width": 120},
#         {"fieldname": "shift_start", "label": "Shift Start", "fieldtype": "Time", "width": 100},
#         {"fieldname": "shift_end", "label": "Shift End", "fieldtype": "Time", "width": 100},
#         {"fieldname": "in_time", "label": "IN Time", "fieldtype": "Time", "width": 120},
#         {"fieldname": "out_time", "label": "OUT Time", "fieldtype": "Time", "width": 120},
#         {
#             "fieldname": "status",
#             "label": "Status",
#             "fieldtype": "Data",
#             "width": 150,
#             "align": "center"
#         }
#     ]

#     # Extract data
#     data = attendance_data.get("data", [])

#     # Attach date to each record and format the Status field with color
#     for entry in data:
#         entry["date"] = date  

#         # Assign color formatting for Status text
#         if entry["status"] == "Present":
#             entry["status"] = f"<span style='color:green;'>{entry['status']}</span>"
#         elif entry["status"] == "Absent":
#             entry["status"] = f"<span style='color:red;'>{entry['status']}</span>"
#         else:  # For Leave Type (e.g., Sick Leave, Casual Leave, etc.)
#             entry["status"] = f"<span style='color:#BDB76B;'>{entry['status']}</span>"

#     return columns, data

import frappe
from frappe.utils import getdate, add_to_date
from mohan_impex.mohan_impex.report.daily_attendance_report import get_employee_attendance_report

def execute(filters=None):
    """
    Generates a Daily Attendance Report including employee details, IN/OUT times, shifts, and attendance status with colored text.
    
    :param filters: Dictionary containing filter options, e.g., {'date': 'YYYY-MM-DD'}
    :return: Tuple (columns, data) formatted for ERPNext report generation.
    """

    # Default date if not provided
    date = filters.get("date") if filters else getdate()
    is_sunday = getdate(date).weekday() == 6  # Check if Sunday

    # Fetch attendance data
    attendance_data = get_employee_attendance_report(date)
    
    if attendance_data.get("status") != "success":
        frappe.throw("Error fetching attendance data: " + attendance_data.get("message", "Unknown error"))

    # Define report columns
    columns = [
        {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "employee", "label": "Employee ID", "fieldtype": "Data", "width": 120},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 150},
        {"fieldname": "shift", "label": "Shift", "fieldtype": "Data", "width": 120},
        {"fieldname": "shift_start", "label": "Shift Start", "fieldtype": "Time", "width": 100},
        {"fieldname": "shift_end", "label": "Shift End", "fieldtype": "Time", "width": 100},
        {"fieldname": "in_time", "label": "IN Time", "fieldtype": "Time", "width": 120},
        {"fieldname": "out_time", "label": "OUT Time", "fieldtype": "Time", "width": 120},
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 150,
            "align": "center"
        }
    ]

    # Extract data
    data = attendance_data.get("data", [])

    # Apply status & color formatting
    for entry in data:
        entry["date"] = date  

        if entry["status"] == "Present":
            entry["status"] = f"<span style='color:green;'>{entry['status']}</span>"
        elif entry["status"] == "Absent":
            entry["status"] = f"<span style='color:red;'>{entry['status']}</span>"
        elif entry["status"] == "Weekly Off":
            entry["status"] = f"<span style='color:#BDB76B;'>{entry['status']}</span>"
        elif entry["status"] == "Compensatory Work":
            entry["status"] = f"<span style='color:blue;'>{entry['status']}</span>"
        else:  # Leave Types
            entry["status"] = f"<span style='color:#BDB76B;'>{entry['status']}</span>"

    return columns, data


