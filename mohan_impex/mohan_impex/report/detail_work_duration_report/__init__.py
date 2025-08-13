# import frappe
# from frappe.utils import getdate

# @frappe.whitelist()
# def get_employee_attendance_report(date=None):
#     """
#     Fetches employee attendance details including shift details, IN/OUT times, leave status, holidays,
#     and additional employee details (Branch, Reports To, Custom Reports Two, Company).

#     :param date: (Optional) Date in 'YYYY-MM-DD' format. Defaults to today.
#     :return: JSON response containing employee attendance details.
#     """
#     try:
#         if not date:
#             date = getdate()  # Default to today's date
        
#         is_sunday = getdate(date).weekday() == 6  # Check if Sunday

#         # Fetch employee attendance data including additional details
#         checkins = frappe.db.sql("""
#             SELECT 
#                 emp.name AS employee,
#                 emp.employee_name,
#                 emp.department,
#                 emp.branch,
#                 emp.reports_to,
#                 emp.custom_reports_one_name,
#                 emp.custom_reports_two_name,
#                 emp.custom_reports_two,  -- Assuming this is a valid custom field
#                 emp.company,
#                 emp.holiday_list,  -- Fetch assigned holiday list
#                 chk.shift,
#                 chk.shift_start,
#                 chk.shift_end,
#                 chk.log_type,
#                 chk.time AS log_time
#             FROM `tabEmployee` AS emp
#             LEFT JOIN `tabEmployee Checkin` AS chk 
#                 ON emp.name = chk.employee 
#                 AND DATE(chk.time) = %s
#             WHERE emp.status = 'Active'
#             ORDER BY emp.name, chk.time
#         """, (date,), as_dict=True)

#         # Fetch Approved Leaves covering the given date
#         approved_leaves = frappe.db.get_all(
#             'Leave Application',
#             filters={
#                 'status': 'Approved',
#                 'from_date': ['<=', date],
#                 'to_date': ['>=', date]
#             },
#             fields=['employee', 'leave_type']
#         )

#         # Convert leave list to dictionary for quick lookup
#         leave_map = {leave["employee"]: leave["leave_type"] for leave in approved_leaves}

#         # Fetch holidays from holiday list
#         holiday_map = {}
#         for employee in checkins:
#             if employee["holiday_list"]:
#                 holiday = frappe.db.get_value(
#                     "Holiday",
#                     {"parent": employee["holiday_list"], "holiday_date": date},
#                     ["description"]
#                 )
#                 if holiday:
#                     holiday_map[employee["employee"]] = holiday

#         # Organizing employee attendance with IN/OUT times and Status
#         attendance_records = {}
#         for entry in checkins:
#             emp_id = entry["employee"]
#             if emp_id not in attendance_records:
#                 attendance_records[emp_id] = {
#                     "employee": emp_id,
#                     "employee_name": entry["employee_name"],
#                     "department": entry["department"][:-7] if entry["department"] and len(entry["department"]) > 9 else "",
#                     "branch": entry["branch"],
#                     "reports_to": entry["reports_to"],
#                     "custom_reports_two": entry["custom_reports_two"],
#                     "company": entry["company"],
#                     "shift": entry["shift"],
#                     "shift_start": entry["shift_start"],
#                     "shift_end": entry["shift_end"],
#                     "in_time": None,
#                     "out_time": None,
#                     "status": "Weekly Off" if is_sunday else "Absent"
#                 }
            
#             if entry["log_type"] == "IN":
#                 attendance_records[emp_id]["in_time"] = entry["log_time"]
#             elif entry["log_type"] == "OUT":
#                 attendance_records[emp_id]["out_time"] = entry["log_time"]

#         # Assign Attendance Status and Format Times
#         for emp_id, record in attendance_records.items():
#             if is_sunday:
#                 if record["in_time"]:  # If check-in found on Sunday
#                     record["status"] = "Compensatory Work"
#                 else:
#                     record["status"] = "Weekly Off"
#             elif emp_id in holiday_map:
#                 record["status"] = f"Holiday - {holiday_map[emp_id]}"  # Assign Holiday Name
#             else:
#                 if emp_id in leave_map:
#                     record["status"] = leave_map[emp_id]  # Assign Leave Type
#                 elif record["in_time"]:
#                     record["status"] = "Present"

#             # Convert datetime objects to "HH:MM:SS" format if not None
#             record["shift_start"] = record["shift_start"].strftime("%H:%M:%S") if record["shift_start"] else None
#             record["shift_end"] = record["shift_end"].strftime("%H:%M:%S") if record["shift_end"] else None
#             record["in_time"] = record["in_time"].strftime("%H:%M:%S") if record["in_time"] else None
#             record["out_time"] = record["out_time"].strftime("%H:%M:%S") if record["out_time"] else None
        
#         return {"status": "success", "date": date, "data": list(attendance_records.values())}
    
#     except Exception as e:
#         frappe.log_error(f"Error in get_employee_attendance_report: {str(e)}", "Attendance Report API")
#         return {"status": "error", "message": str(e)}



import frappe
from frappe.utils import getdate

@frappe.whitelist()
def get_employee_attendance_report(date=None):
    """
    Returns attendance + employee attributes for a specific date.
    """
    try:
        if not date:
            date = getdate()

        is_sunday = getdate(date).weekday() == 6

        checkins = frappe.db.sql("""
            SELECT 
                emp.name AS employee,
                emp.employee_name,
                emp.department,
                emp.branch,
                emp.reports_to,
                emp.custom_reports_one_name,
                emp.custom_reports_two_name,
                emp.custom_reports_two,      -- Link to Employee (Reports Two)
                emp.company,
                emp.holiday_list,
                chk.shift,
                chk.shift_start,
                chk.shift_end,
                chk.log_type,
                chk.time AS log_time
            FROM `tabEmployee` AS emp
            LEFT JOIN `tabEmployee Checkin` AS chk 
                ON emp.name = chk.employee 
               AND DATE(chk.time) = %s
            WHERE emp.status = 'Active'
            ORDER BY emp.name, chk.time
        """, (date,), as_dict=True)

        # Approved leaves on this date
        approved_leaves = frappe.db.get_all(
            'Leave Application',
            filters={
                'status': 'Approved',
                'from_date': ['<=', date],
                'to_date': ['>=', date]
            },
            fields=['employee', 'leave_type']
        )
        leave_map = {l["employee"]: l["leave_type"] for l in approved_leaves}

        # Holidays
        holiday_map = {}
        for e in checkins:
            if e.get("holiday_list"):
                holiday = frappe.db.get_value(
                    "Holiday",
                    {"parent": e["holiday_list"], "holiday_date": date},
                    ["description"]
                )
                if holiday:
                    holiday_map[e["employee"]] = holiday

        attendance_records = {}
        for entry in checkins:
            emp_id = entry["employee"]
            if emp_id not in attendance_records:
                attendance_records[emp_id] = {
                    "employee": emp_id,
                    "employee_name": entry.get("employee_name"),
                    "department": entry.get("department"),   # no trimming
                    "branch": entry.get("branch"),
                    "reports_to": entry.get("reports_to"),
                    "custom_reports_two": entry.get("custom_reports_two"),
                    "company": entry.get("company"),
                    "shift": entry.get("shift"),
                    "shift_start": entry.get("shift_start"),
                    "shift_end": entry.get("shift_end"),
                    "in_time": None,
                    "out_time": None,
                    "status": "Weekly Off" if is_sunday else "Absent",
                }

            if entry.get("log_type") == "IN":
                attendance_records[emp_id]["in_time"] = entry.get("log_time")
            elif entry.get("log_type") == "OUT":
                attendance_records[emp_id]["out_time"] = entry.get("log_time")

        # status resolution + stringify times
        for emp_id, record in attendance_records.items():
            if is_sunday:
                record["status"] = "Compensatory Work" if record.get("in_time") else "Weekly Off"
            elif emp_id in holiday_map:
                record["status"] = f"Holiday - {holiday_map[emp_id]}"
            else:
                if emp_id in leave_map:
                    record["status"] = leave_map[emp_id]
                elif record.get("in_time"):
                    record["status"] = "Present"

            # Keep as time strings for report
            record["shift_start"] = record["shift_start"].strftime("%H:%M:%S") if record.get("shift_start") else None
            record["shift_end"]   = record["shift_end"].strftime("%H:%M:%S") if record.get("shift_end") else None
            record["in_time"]     = record["in_time"].strftime("%H:%M:%S") if record.get("in_time") else None
            record["out_time"]    = record["out_time"].strftime("%H:%M:%S") if record.get("out_time") else None

        return {"status": "success", "date": date, "data": list(attendance_records.values())}

    except Exception as e:
        frappe.log_error(f"Error in get_employee_attendance_report: {str(e)}", "Attendance Report API")
        return {"status": "error", "message": str(e)}
