# import frappe
# from mohan_impex.mohan_impex.report.monthly_attendance_report import get_employee_attendance_report

# def execute(filters=None):
#     """
#     Fetches employee attendance report with summarized data.
#     """
#     if not filters or not filters.get("start_date") or not filters.get("end_date"):
#         frappe.throw("Please select Start Date and End Date.")

#     start_date = filters.get("start_date")
#     end_date = filters.get("end_date")

#     response = get_employee_attendance_report(start_date, end_date)

#     if response.get("status") != "success":
#         frappe.throw(response.get("message"))

#     data = response.get("data", [])

#     # Define Columns
#     columns = [
#         {"fieldname": "Employee ID", "label": "Employee ID", "fieldtype": "Link", "options": "Employee", "width": 120},
#         {"fieldname": "Employee Name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
#         {"fieldname": "Department", "label": "Department", "fieldtype": "Data", "width": 120},
#         {"fieldname": "Branch", "label": "Branch", "fieldtype": "Data", "width": 120},
#         {"fieldname": "Reports To", "label": "Reports To", "fieldtype": "Data", "width": 120},
#         {"fieldname": "Company", "label": "Company", "fieldtype": "Data", "width": 120}
#     ]

#     # Add Date Columns
#     date_keys = [key for key in data[0].keys() if key not in ["Employee ID", "Employee Name", "Department", "Branch", "Reports To", "Company", "Summary"]]
#     for date in date_keys:
#         columns.append({"fieldname": date, "label": date, "fieldtype": "Data", "width": 100})

#     # Add Summary Column
#     columns.append({"fieldname": "Summary", "label": "Summary", "fieldtype": "Data", "width": 250})

#     return columns, data


import frappe
from mohan_impex.mohan_impex.report.monthly_attendance_report import get_employee_attendance_report

def execute(filters=None):
    """
    Fetches employee attendance report with summarized data.
    """
    if not filters or not filters.get("start_date") or not filters.get("end_date"):
        frappe.throw("Please select Start Date and End Date.")

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")

    response = get_employee_attendance_report(start_date, end_date)

    if response.get("status") != "success":
        frappe.throw(response.get("message"))

    data = response.get("data", [])

    # Define Static Columns (Employee Details)
    columns = [
        {"fieldname": "Employee ID", "label": "Employee ID", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"fieldname": "Employee Name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "Department", "label": "Department", "fieldtype": "Data", "width": 120},
        {"fieldname": "Branch", "label": "Location", "fieldtype": "Data", "width": 120},
        # {"fieldname": "Reports To", "label": "Reports To", "fieldtype": "Data", "width": 120},
        # {"fieldname": "Company", "label": "Company", "fieldtype": "Data", "width": 120}
    ]

    # Identify Date Columns Dynamically
    date_keys = [key for key in data[0].keys() if key not in ["Employee ID", "Employee Name", "Department", "Branch", "Reports To", "Company", "Summary"]]
    
    # Sort dates correctly
    date_keys.sort()

    # Add Date Columns
    for date in date_keys:
        columns.append({"fieldname": date, "label": date, "fieldtype": "Data", "width": 100})

    # Add Summary Column
    columns.append({"fieldname": "Summary", "label": "Count", "fieldtype": "Data", "width": 450})

    return columns, data
