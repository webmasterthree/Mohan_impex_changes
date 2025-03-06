# import frappe
# from frappe.utils import getdate, format_time, time_diff_in_hours
# from mohan_impex.mohan_impex.report.detail_work_duration_report import get_employee_attendance_report

# def format_date(date_str):
#     """Formats a date from YYYY-MM-DD to DD-MMM-YYYY"""
#     try:
#         return frappe.utils.get_datetime(date_str).strftime("%d-%b-%Y")
#     except:
#         return date_str

# def execute(filters=None):
#     """
#     Generates the Detail Work Duration Report in the required row-wise format.
#     """
#     if not filters:
#         filters = {}

#     start_date = filters.get("start_date")
#     end_date = filters.get("end_date")
#     selected_employee = filters.get("employee")
#     selected_department = filters.get("department")
#     selected_branch = filters.get("branch")
#     selected_reports_to = filters.get("reports_to")
#     selected_company = filters.get("company")
#     selected_shift = filters.get("shift")

#     if not start_date or not end_date:
#         frappe.throw("Please select both Start Date and End Date.")

#     start_date = getdate(start_date)
#     end_date = getdate(end_date)

#     # Initialize attendance data storage
#     attendance_data = {}
#     date_headers = []

#     current_date = start_date
#     while current_date <= end_date:
#         formatted_date = format_date(str(current_date))
#         date_headers.append(formatted_date)

#         response = get_employee_attendance_report(str(current_date))

#         if response.get("status") == "error":
#             frappe.throw(f"Error fetching data: {response.get('message')}")

#         for record in response.get("data", []):
#             # Apply selected filters
#             if selected_employee and record["employee"] != selected_employee:
#                 continue
#             if selected_department and record["department"] != selected_department:
#                 continue
#             if selected_branch and record["branch"] != selected_branch:
#                 continue
#             if selected_reports_to and record["reports_to"] != selected_reports_to:
#                 continue
#             if selected_company and record["company"] != selected_company:
#                 continue
#             if selected_shift and record["shift"] != selected_shift:
#                 continue

#             emp_id = record["employee"]

#             if emp_id not in attendance_data:
#                 attendance_data[emp_id] = {
#                     "Employee ID": record["employee"],
#                     "Employee Name": record["employee_name"],
#                     "Department": record["department"],
#                     "Branch": record["branch"],
#                     "Reports To": record["reports_to"],
#                     "Company": record["company"],
#                     "Shift": record["shift"],
#                     "Shift Start": format_time(record["shift_start"]) if record.get("shift_start") else "",
#                     "Shift End": format_time(record["shift_end"]) if record.get("shift_end") else "",
#                     "Attendance": {}
#                 }

#             check_in = format_time(record["in_time"]) if record["in_time"] else ""
#             check_out = format_time(record["out_time"]) if record["out_time"] else ""
            
#             # Calculate Total Hours Worked
#             total_hours = ""
#             over_time = ""
#             late_by = ""
#             early_by = ""

#             if record["in_time"] and record["out_time"]:
#                 total_hours = round(time_diff_in_hours(record["in_time"], record["out_time"]), 2)
#                 shift_start = record.get("shift_start")
#                 shift_end = record.get("shift_end")

#                 if shift_start:
#                     late_by = round(time_diff_in_hours(shift_start, record["in_time"]), 2) if record["in_time"] > shift_start else ""
#                 if shift_end:
#                     early_by = round(time_diff_in_hours(record["out_time"], shift_end), 2) if record["out_time"] < shift_end else ""
#                 if shift_end and record["out_time"] > shift_end:
#                     over_time = round(time_diff_in_hours(record["out_time"], shift_end), 2)

#             attendance_data[emp_id]["Attendance"][formatted_date] = {
#                 "Check-In": check_in,
#                 "Check-Out": check_out,
#                 "Status": "P" if record["status"] == "Present" else "A" if record["status"] == "Absent" else "H",
#                 "Total Hours": total_hours,
#                 "Over Time": over_time,
#                 "Late By": late_by,
#                 "Early By": early_by
#             }

#         current_date = frappe.utils.add_days(current_date, 1)

#     # Transform data into required format
#     final_data = transform_to_required_format(attendance_data, date_headers)

#     # Generate columns dynamically
#     columns = [
#         {"label": "Employee ID", "fieldname": "Employee ID", "fieldtype": "Data", "width": 120},
#         {"label": "Employee Name", "fieldname": "Employee Name", "fieldtype": "Data", "width": 150},
#         {"label": "Department", "fieldname": "Department", "fieldtype": "Data", "width": 120},
#         {"label": "Branch", "fieldname": "Branch", "fieldtype": "Data", "width": 120},
#         {"label": "Reports To", "fieldname": "Reports To", "fieldtype": "Data", "width": 150},
#         {"label": "Company", "fieldname": "Company", "fieldtype": "Data", "width": 150},
#         {"label": "Shift", "fieldname": "Shift", "fieldtype": "Data", "width": 120},
#         {"label": "Shift Start", "fieldname": "Shift Start", "fieldtype": "Time", "width": 120},
#         {"label": "Shift End", "fieldname": "Shift End", "fieldtype": "Time", "width": 120}
#     ]

#     for formatted_date in date_headers:
#         columns.append({"label": formatted_date, "fieldname": formatted_date, "fieldtype": "Data", "width": 150})

#     return columns, final_data

# def transform_to_required_format(attendance_data, date_headers):
#     """
#     Transforms the attendance data into the required format.
#     """
#     final_data = []

#     for emp_id, row in attendance_data.items():
#         # Employee details row (displayed once)
#         employee_info = [
#             row["Employee ID"], row["Employee Name"], row["Department"], row["Branch"],
#             row["Reports To"], row["Company"], row["Shift"], row["Shift Start"], row["Shift End"]
#         ]

#         # Create row-wise structured data
#         days_row = employee_info + date_headers
#         checkin_row = ["Check-In"] + ["-"] * (len(employee_info) - 1)
#         checkout_row = ["Check-Out"] + ["-"] * (len(employee_info) - 1)
#         status_row = ["Status"] + ["-"] * (len(employee_info) - 1)
#         total_hours_row = ["Total Hours"] + ["-"] * (len(employee_info) - 1)
#         overtime_row = ["Over Time"] + ["-"] * (len(employee_info) - 1)
#         late_by_row = ["Late By"] + ["-"] * (len(employee_info) - 1)
#         early_by_row = ["Early By"] + ["-"] * (len(employee_info) - 1)

#         for date in date_headers:
#             attendance = row["Attendance"].get(date, {})
#             checkin_row.append(attendance.get("Check-In", ""))
#             checkout_row.append(attendance.get("Check-Out", ""))
#             status_row.append(attendance.get("Status", "-"))
#             total_hours_row.append(attendance.get("Total Hours", ""))
#             overtime_row.append(attendance.get("Over Time", ""))
#             late_by_row.append(attendance.get("Late By", ""))
#             early_by_row.append(attendance.get("Early By", ""))

#         # Append rows for this employee
#         final_data.append(days_row)
#         final_data.append(checkin_row)
#         final_data.append(checkout_row)
#         final_data.append(status_row)
#         final_data.append(total_hours_row)
#         final_data.append(overtime_row)
#         final_data.append(late_by_row)
#         final_data.append(early_by_row)

#     return final_data








# import frappe
# from frappe.utils import getdate, format_time, time_diff_in_hours
# from mohan_impex.mohan_impex.report.detail_work_duration_report import get_employee_attendance_report

# def format_date(date_str):
#     """Formats a date from YYYY-MM-DD to DD-MMM-YYYY"""
#     try:
#         return frappe.utils.get_datetime(date_str).strftime("%d-%b-%Y")
#     except:
#         return date_str

# def convert_to_hours_minutes(value):
#     """Converts decimal hours to 'X hours, Y min' format and ensures positive values"""
#     if isinstance(value, (int, float)):
#         hours = abs(int(value))
#         minutes = abs(round((value - int(value)) * 60))
#         return f"{hours} hours, {minutes} min" if hours or minutes else "-"
#     return "-"

# def transform_to_required_format(attendance_data, date_headers):
#     """Transforms the attendance data into a row-wise format per employee, ensuring proper column alignment."""
#     final_data = []
#     for emp_id, record in attendance_data.items():
#         # First row with Employee ID and Details
#         emp_details = [
#             record["Employee ID"], record["Employee Name"], record["Department"], record["Branch"],
#             record["Reports To"], record["Company"], record["Shift"], record["Shift Start"], record["Shift End"]
#         ]
#         final_data.append(emp_details + [""] * len(date_headers))
        
#         # Append Attendance Attributes Below Employee ID
#         for field in ["Check-In", "Check-Out", "Late By", "Early By", "Total Hours", "Over Time", "Status"]:
#             row = [field] + [""] * 8  # Empty columns under employee details
#             for date in date_headers:
#                 row.append(record["Attendance"].get(date, {}).get(field, "-"))
#             final_data.append(row)
#     return final_data

# def execute(filters=None):
#     if not filters:
#         filters = {}

#     start_date = filters.get("start_date")
#     end_date = filters.get("end_date")
    
#     if not start_date or not end_date:
#         frappe.throw("Please select both Start Date and End Date.")

#     start_date = getdate(start_date)
#     end_date = getdate(end_date)

#     attendance_data = {}
#     date_headers = []
    
#     current_date = start_date
#     while current_date <= end_date:
#         formatted_date = format_date(str(current_date))
#         date_headers.append(formatted_date)
#         response = get_employee_attendance_report(str(current_date))
        
#         if response.get("status") == "error":
#             frappe.throw(f"Error fetching data: {response.get('message')}")
        
#         for record in response.get("data", []):
#             emp_id = record["employee"]
#             if emp_id not in attendance_data:
#                 attendance_data[emp_id] = {
#                     "Employee ID": record["employee"],
#                     "Employee Name": record["employee_name"],
#                     "Department": record["department"],
#                     "Branch": record["branch"],
#                     "Reports To": record["reports_to"],
#                     "Company": record["company"],
#                     "Shift": record["shift"],
#                     "Shift Start": format_time(record["shift_start"]) if record.get("shift_start") else "",
#                     "Shift End": format_time(record["shift_end"]) if record.get("shift_end") else "",
#                     "Attendance": {}
#                 }
#             attendance_data[emp_id]["Attendance"].setdefault(formatted_date, {
#                 "Check-In": "-", "Check-Out": "-", "Status": "Absent",
#                 "Total Hours": "-", "Over Time": "-", "Late By": "-", "Early By": "-"
#             })
#             attendance_data[emp_id]["Attendance"][formatted_date].update({
#                 "Check-In": format_time(record["in_time"]) if record["in_time"] else "-",
#                 "Check-Out": format_time(record["out_time"]) if record["out_time"] else "-",
#                 "Status": record.get("status", "Absent"),
#                 "Total Hours": convert_to_hours_minutes(time_diff_in_hours(record["in_time"], record["out_time"])) if record["in_time"] and record["out_time"] else "-",
#                 "Over Time": convert_to_hours_minutes(time_diff_in_hours(record["out_time"], record.get("shift_end"))) if record["out_time"] and record.get("shift_end") and record["out_time"] > record["shift_end"] else "-",
#                 "Late By": convert_to_hours_minutes(time_diff_in_hours(record.get("shift_start"), record["in_time"])) if record.get("shift_start") and record["in_time"] and record["in_time"] > record["shift_start"] else "-",
#                 "Early By": convert_to_hours_minutes(time_diff_in_hours(record["out_time"], record.get("shift_end"))) if record["out_time"] and record.get("shift_end") and record["out_time"] < record["shift_end"] else "-"
#             })
        
#         current_date = frappe.utils.add_days(current_date, 1)

#     final_data = transform_to_required_format(attendance_data, date_headers)
    
#     columns = [
#         "Employee ID", "Employee Name", "Department", "Branch", "Reports To", "Company", "Shift", "Shift Start", "Shift End"
#     ] + date_headers
    
#     return columns, final_data

import frappe
from frappe.utils import getdate, format_time, time_diff_in_hours
from mohan_impex.mohan_impex.report.detail_work_duration_report import get_employee_attendance_report

def format_date(date_str):
    """Formats a date from YYYY-MM-DD to DD-MMM-YYYY"""
    try:
        return frappe.utils.get_datetime(date_str).strftime("%d-%b-%Y")
    except:
        return date_str

def convert_to_hours_minutes(value):
    """Converts decimal hours to 'X hours, Y min' format and ensures positive values"""
    if isinstance(value, (int, float)):
        hours = abs(int(value))
        minutes = abs(round((value - int(value)) * 60))
        return f"{hours} hours, {minutes} min" if hours or minutes else "-"
    return "-"

def transform_to_required_format(attendance_data, date_headers):
    """Transforms the attendance data into a row-wise format per employee, ensuring proper column alignment."""
    final_data = []
    for emp_id, record in attendance_data.items():
        emp_details = [
            record["Employee ID"], record["Employee Name"], record["Department"], record["Branch"],
            record["Reports To"], record["Company"], record["Shift"], record["Shift Start"], record["Shift End"]
        ]
        final_data.append(emp_details + [""] * len(date_headers))
        
        for field in ["Check-In", "Check-Out", "Late By", "Early By", "Total Hours", "Over Time", "Status"]:
            row = [field] + [""] * 8  
            for date in date_headers:
                row.append(record["Attendance"].get(date, {}).get(field, "-"))
            final_data.append(row)
    return final_data

def execute(filters=None):
    if not filters:
        filters = {}

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    selected_employee = filters.get("employee")
    selected_department = filters.get("department")
    selected_branch = filters.get("branch")
    selected_reports_to = filters.get("reports_to")
    selected_company = filters.get("company")
    selected_shift = filters.get("shift")

    if not start_date or not end_date:
        frappe.throw("Please select both Start Date and End Date.")

    start_date = getdate(start_date)
    end_date = getdate(end_date)

    attendance_data = {}
    date_headers = []
    
    current_date = start_date
    while current_date <= end_date:
        formatted_date = format_date(str(current_date))
        date_headers.append(formatted_date)
        response = get_employee_attendance_report(str(current_date))
        
        if response.get("status") == "error":
            frappe.throw(f"Error fetching data: {response.get('message')}")
        
        for record in response.get("data", []):
            if selected_employee and record["employee"] != selected_employee:
                continue
            if selected_department and record["department"] != selected_department:
                continue
            if selected_branch and record["branch"] != selected_branch:
                continue
            if selected_reports_to and record["reports_to"] != selected_reports_to:
                continue
            if selected_company and record["company"] != selected_company:
                continue
            if selected_shift and record["shift"] != selected_shift:
                continue

            emp_id = record["employee"]
            if emp_id not in attendance_data:
                attendance_data[emp_id] = {
                    "Employee ID": record["employee"],
                    "Employee Name": record["employee_name"],
                    "Department": record["department"],
                    "Branch": record["branch"],
                    "Reports To": record["reports_to"],
                    "Company": record["company"],
                    "Shift": record["shift"],
                    "Shift Start": format_time(record["shift_start"]) if record.get("shift_start") else "",
                    "Shift End": format_time(record["shift_end"]) if record.get("shift_end") else "",
                    "Attendance": {}
                }
            attendance_data[emp_id]["Attendance"].setdefault(formatted_date, {
                "Check-In": "-", "Check-Out": "-", "Status": "Absent",
                "Total Hours": "-", "Over Time": "-", "Late By": "-", "Early By": "-"
            })
            attendance_data[emp_id]["Attendance"][formatted_date].update({
                "Check-In": format_time(record["in_time"]) if record["in_time"] else "-",
                "Check-Out": format_time(record["out_time"]) if record["out_time"] else "-",
                "Status": record.get("status", "Absent"),
                "Total Hours": convert_to_hours_minutes(time_diff_in_hours(record["in_time"], record["out_time"])) if record["in_time"] and record["out_time"] else "-",
                "Over Time": convert_to_hours_minutes(time_diff_in_hours(record["out_time"], record.get("shift_end"))) if record["out_time"] and record.get("shift_end") and record["out_time"] > record["shift_end"] else "-",
                "Late By": convert_to_hours_minutes(time_diff_in_hours(record.get("shift_start"), record["in_time"])) if record.get("shift_start") and record["in_time"] and record["in_time"] > record["shift_start"] else "-",
                "Early By": convert_to_hours_minutes(time_diff_in_hours(record["out_time"], record.get("shift_end"))) if record["out_time"] and record.get("shift_end") and record["out_time"] < record["shift_end"] else "-"
            })
        
        current_date = frappe.utils.add_days(current_date, 1)

    final_data = transform_to_required_format(attendance_data, date_headers)
    
    columns = [
        "Employee ID", "Employee Name", "Department", "Branch", "Reports To", "Company", "Shift", "Shift Start", "Shift End"
    ] + date_headers
    
    return columns, final_data