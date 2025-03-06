# import frappe
# from frappe.utils import getdate
# from datetime import datetime

# @frappe.whitelist()
# def get_employee_attendance_report(date=None):
#     """
#     Fetches employee attendance details including shift details, IN/OUT times, and leave status.

#     :param date: (Optional) Date in 'YYYY-MM-DD' format. Defaults to today.
#     :return: JSON response containing employee attendance details.
#     """
#     try:
#         if not date:
#             date = getdate()  # Default to today's date
        
#         # Fetch employee attendance data including IN/OUT times and shift details
#         checkins = frappe.db.sql("""
#             SELECT 
#                 emp.name AS employee,
#                 emp.employee_name,
#                 emp.department,
#                 chk.shift,
#                 chk.shift_start,
#                 chk.shift_end,
#                 chk.log_type,
#                 chk.time AS log_time
#             FROM `tabEmployee` AS emp
#             LEFT JOIN `tabEmployee Checkin` AS chk 
#                 ON emp.name = chk.employee 
#                 AND DATE(chk.time) = %s
#             ORDER BY emp.name, chk.time
#         """, (date,), as_dict=True)

#         # Fetch Approved Leaves covering the given date
#         approved_leaves = frappe.db.get_all(
#             'Leave Application',
#             filters={
#                 'status': 'Approved',
#                 'from_date': ['<=', date],  # Leave started before or on the given date
#                 'to_date': ['>=', date]  # Leave is still valid on the given date
#             },
#             fields=['employee', 'leave_type']
#         )

#         # Convert leave list to dictionary for quick lookup
#         leave_map = {leave["employee"]: leave["leave_type"] for leave in approved_leaves}

#         # Organizing employee attendance with IN/OUT times and Status
#         attendance_records = {}
#         for entry in checkins:
#             emp_id = entry["employee"]
#             if emp_id not in attendance_records:
#                 attendance_records[emp_id] = {
#                     "employee": emp_id,
#                     "employee_name": entry["employee_name"],
#                     "department": entry["department"][:-9] if entry["department"] and len(entry["department"]) > 9 else "",  # Remove last 9 characters
#                     "shift": entry["shift"],
#                     "shift_start": entry["shift_start"],
#                     "shift_end": entry["shift_end"],
#                     "in_time": None,
#                     "out_time": None,
#                     "status": "Absent"  # Default to Absent, updated later if needed
#                 }
#             if entry["log_type"] == "IN":
#                 attendance_records[emp_id]["in_time"] = entry["log_time"]
#             elif entry["log_type"] == "OUT":
#                 attendance_records[emp_id]["out_time"] = entry["log_time"]

#         # Assign Attendance Status and Format Times
#         for emp_id, record in attendance_records.items():
#             if emp_id in leave_map:
#                 record["status"] = leave_map[emp_id]  # Assign Leave Type
#             elif record["in_time"]:
#                 record["status"] = "Present"  # Mark as Present
            
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
from datetime import datetime

@frappe.whitelist()
def get_employee_attendance_report(date=None):
    """
    Fetches employee attendance details including shift details, IN/OUT times, and leave status.

    :param date: (Optional) Date in 'YYYY-MM-DD' format. Defaults to today.
    :return: JSON response containing employee attendance details.
    """
    try:
        if not date:
            date = getdate()  # Default to today's date
        
        is_sunday = getdate(date).weekday() == 6  # Check if Sunday

        # Fetch employee attendance data including IN/OUT times and shift details
        checkins = frappe.db.sql("""
            SELECT 
                emp.name AS employee,
                emp.employee_name,
                emp.department,
                chk.shift,
                chk.shift_start,
                chk.shift_end,
                chk.log_type,
                chk.time AS log_time
            FROM `tabEmployee` AS emp
            LEFT JOIN `tabEmployee Checkin` AS chk 
                ON emp.name = chk.employee 
                AND DATE(chk.time) = %s
            ORDER BY emp.name, chk.time
        """, (date,), as_dict=True)

        # Fetch Approved Leaves covering the given date
        approved_leaves = frappe.db.get_all(
            'Leave Application',
            filters={
                'status': 'Approved',
                'from_date': ['<=', date],
                'to_date': ['>=', date]
            },
            fields=['employee', 'leave_type']
        )

        # Convert leave list to dictionary for quick lookup
        leave_map = {leave["employee"]: leave["leave_type"] for leave in approved_leaves}

        # Organizing employee attendance with IN/OUT times and Status
        attendance_records = {}
        for entry in checkins:
            emp_id = entry["employee"]
            if emp_id not in attendance_records:
                attendance_records[emp_id] = {
                    "employee": emp_id,
                    "employee_name": entry["employee_name"],
                    "department": entry["department"][:-9] if entry["department"] and len(entry["department"]) > 9 else "",
                    "shift": entry["shift"],
                    "shift_start": entry["shift_start"],
                    "shift_end": entry["shift_end"],
                    "in_time": None,
                    "out_time": None,
                    "status": "Weekly Off" if is_sunday else "Absent"
                }
            
            if entry["log_type"] == "IN":
                attendance_records[emp_id]["in_time"] = entry["log_time"]
            elif entry["log_type"] == "OUT":
                attendance_records[emp_id]["out_time"] = entry["log_time"]

        # Assign Attendance Status and Format Times
        for emp_id, record in attendance_records.items():
            if is_sunday:
                if record["in_time"]:  # If check-in found on Sunday
                    record["status"] = "Compensatory Work"
                else:
                    record["status"] = "Weekly Off"
            else:
                if emp_id in leave_map:
                    record["status"] = leave_map[emp_id]  # Assign Leave Type
                elif record["in_time"]:
                    record["status"] = "Present"

            # Convert datetime objects to "HH:MM:SS" format if not None
            record["shift_start"] = record["shift_start"].strftime("%H:%M:%S") if record["shift_start"] else None
            record["shift_end"] = record["shift_end"].strftime("%H:%M:%S") if record["shift_end"] else None
            record["in_time"] = record["in_time"].strftime("%H:%M:%S") if record["in_time"] else None
            record["out_time"] = record["out_time"].strftime("%H:%M:%S") if record["out_time"] else None
        
        return {"status": "success", "date": date, "data": list(attendance_records.values())}
    
    except Exception as e:
        frappe.log_error(f"Error in get_employee_attendance_report: {str(e)}", "Attendance Report API")
        return {"status": "error", "message": str(e)}

