import frappe
from datetime import datetime, timedelta
from collections import defaultdict

@frappe.whitelist()
def get_overtime_checkins(from_date=None, to_date=None):
    if not from_date or not to_date:
        frappe.throw("Please provide both from_date and to_date in 'yyyy-mm-dd' format.")

    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
    except ValueError:
        frappe.throw("Invalid date format. Please use 'yyyy-mm-dd'.")

    query = """
        SELECT 
            ec.employee,
            e.employee_name,
            ec.shift,
            ec.shift_start,
            ec.shift_end,
            ec.log_type,
            ec.time
        FROM 
            `tabEmployee Checkin` ec
        INNER JOIN 
            `tabEmployee` e ON ec.employee = e.name
        WHERE 
            e.custom_allow_overtime = 1
            AND ec.time BETWEEN %s AND %s
        ORDER BY ec.employee, ec.time
    """
    raw_data = frappe.db.sql(query, (from_dt, to_dt), as_dict=True)

    checkin_map = defaultdict(list)
    for row in raw_data:
        checkin_map[row['employee']].append(row)

    employee_overtime_summary = defaultdict(lambda: {
        "employee": "",
        "employee_name": "",
        "total_overtime_hours": 0
    })

    for employee, logs in checkin_map.items():
        in_time = None
        shift_hours = 0
        emp_name = ""

        for log in logs:
            emp_name = log["employee_name"]

            if log.get('shift_start') and log.get('shift_end'):
                shift_start = log['shift_start']
                shift_end = log['shift_end']
                if shift_end < shift_start:
                    shift_end += timedelta(days=1)
                shift_hours = round((shift_end - shift_start).total_seconds() / 3600, 2)

            if log['log_type'] == 'IN':
                in_time = log['time']
            elif log['log_type'] == 'OUT' and in_time:
                out_time = log['time']
                worked_hours = round((out_time - in_time).total_seconds() / 3600, 2)
                overtime_hours = max(0, worked_hours - shift_hours)

                # Convert to integer (truncate)
                overtime_hours = int(overtime_hours)

                employee_overtime_summary[employee]["employee"] = employee
                employee_overtime_summary[employee]["employee_name"] = emp_name
                employee_overtime_summary[employee]["total_overtime_hours"] += overtime_hours

                in_time = None

    return list(employee_overtime_summary.values())


# import frappe
# from frappe import _
# from datetime import datetime, timedelta

# @frappe.whitelist()
# def get_employee_checkins(from_date: str = None, to_date: str = None):
#     """Fetch first IN, last OUT, total work duration, overtime, and short time for employee check-ins within a date range."""
#     try:
#         filters = {}
#         if from_date and to_date:
#             filters["time"] = ["between", [from_date, to_date]]
#         elif from_date:
#             filters["time"] = [">=", from_date]
#         elif to_date:
#             filters["time"] = ["<=", to_date]

#         checkins = frappe.db.get_all(
#             'Employee Checkin',
#             fields=["employee", "employee_name", "shift", "shift_start", "shift_end", "log_type", "time"],
#             filters=filters,
#             order_by="employee, time"
#         )

#         employee_checkin_dict = {}

#         # Process Check-ins in a single loop
#         for checkin in checkins:
#             emp_id = checkin["employee"]
            
#             # Handle None values before conversion
#             shift_start = checkin.get("shift_start")
#             shift_end = checkin.get("shift_end")
#             time = checkin.get("time")

#             if not shift_start or not shift_end or not time:
#                 frappe.log_error(f"Missing shift or time data for employee {emp_id}", "Employee Checkin Data Issue")
#                 continue  # Skip this record if shift data is missing

#             # Ensure datetime conversion only if needed
#             shift_start = shift_start if isinstance(shift_start, datetime) else datetime.strptime(shift_start, "%Y-%m-%d %H:%M:%S")
#             shift_end = shift_end if isinstance(shift_end, datetime) else datetime.strptime(shift_end, "%Y-%m-%d %H:%M:%S")
#             time = time if isinstance(time, datetime) else datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

#             # Initialize Employee Record
#             if emp_id not in employee_checkin_dict:
#                 employee_checkin_dict[emp_id] = {
#                     "employee": checkin["employee"],
#                     "employee_name": checkin["employee_name"],
#                     "shift_start": shift_start,
#                     "shift_end": shift_end,
#                     "IN_time": None,
#                     "OUT_time": None,
#                     "work_duration": timedelta(0),
#                     "overtime_hours": 0.0,  # Now stored as float
#                     "shortfall_hours": 0.0
#                 }

#             # Capture first IN and last OUT
#             if checkin["log_type"] == "IN":
#                 if employee_checkin_dict[emp_id]["IN_time"] is None or time < employee_checkin_dict[emp_id]["IN_time"]:
#                     employee_checkin_dict[emp_id]["IN_time"] = time
#             elif checkin["log_type"] == "OUT":
#                 if employee_checkin_dict[emp_id]["OUT_time"] is None or time > employee_checkin_dict[emp_id]["OUT_time"]:
#                     employee_checkin_dict[emp_id]["OUT_time"] = time

#         # Calculate work duration, overtime, and short time
#         for emp_id, record in employee_checkin_dict.items():
#             in_time = record["IN_time"]
#             out_time = record["OUT_time"]
#             shift_start = record["shift_start"]
#             shift_end = record["shift_end"]

#             if in_time and out_time:
#                 actual_work_duration = out_time - in_time
#                 expected_work_duration = shift_end - shift_start

#                 # Calculate overtime & shortfall
#                 if actual_work_duration > expected_work_duration:
#                     record["overtime_hours"] = round(actual_work_duration.total_seconds() / 3600 - expected_work_duration.total_seconds() / 3600, 2)
#                     record["shortfall_hours"] = 0.0
#                 elif actual_work_duration < expected_work_duration:
#                     record["shortfall_hours"] = round(expected_work_duration.total_seconds() / 3600 - actual_work_duration.total_seconds() / 3600, 2)
#                     record["overtime_hours"] = 0.0

#         return {"status": "success", "data": list(employee_checkin_dict.values())}

#     except Exception as e:
#         frappe.log_error(f"Error in get_employee_checkins: {str(e)}", "Employee Checkin API")
#         return {"status": "error", "message": _("Something went wrong"), "error": str(e)}
