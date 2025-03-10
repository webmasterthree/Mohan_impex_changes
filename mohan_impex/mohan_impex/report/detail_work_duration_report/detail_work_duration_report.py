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


