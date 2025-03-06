import frappe
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist()
def get_employee_checkins(from_date: str = None, to_date: str = None):
    """Fetch first IN, last OUT, total work duration, overtime, and short time for employee check-ins within a date range."""
    try:
        filters = {}
        if from_date and to_date:
            filters["time"] = ["between", [from_date, to_date]]
        elif from_date:
            filters["time"] = [">=", from_date]
        elif to_date:
            filters["time"] = ["<=", to_date]

        checkins = frappe.db.get_all(
            'Employee Checkin',
            fields=["employee", "employee_name", "shift", "shift_start", "shift_end", "log_type", "time"],
            filters=filters,
            order_by="employee, time"
        )

        employee_checkin_dict = {}

        # Process Check-ins in a single loop
        for checkin in checkins:
            emp_id = checkin["employee"]
            
            # Handle None values before conversion
            shift_start = checkin.get("shift_start")
            shift_end = checkin.get("shift_end")
            time = checkin.get("time")

            if not shift_start or not shift_end or not time:
                frappe.log_error(f"Missing shift or time data for employee {emp_id}", "Employee Checkin Data Issue")
                continue  # Skip this record if shift data is missing

            # Ensure datetime conversion only if needed
            shift_start = shift_start if isinstance(shift_start, datetime) else datetime.strptime(shift_start, "%Y-%m-%d %H:%M:%S")
            shift_end = shift_end if isinstance(shift_end, datetime) else datetime.strptime(shift_end, "%Y-%m-%d %H:%M:%S")
            time = time if isinstance(time, datetime) else datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

            # Initialize Employee Record
            if emp_id not in employee_checkin_dict:
                employee_checkin_dict[emp_id] = {
                    "employee": checkin["employee"],
                    "employee_name": checkin["employee_name"],
                    "shift_start": shift_start,
                    "shift_end": shift_end,
                    "IN_time": None,
                    "OUT_time": None,
                    "work_duration": timedelta(0),
                    "overtime_hours": 0.0,  # Now stored as float
                    "shortfall_hours": 0.0
                }

            # Capture first IN and last OUT
            if checkin["log_type"] == "IN":
                if employee_checkin_dict[emp_id]["IN_time"] is None or time < employee_checkin_dict[emp_id]["IN_time"]:
                    employee_checkin_dict[emp_id]["IN_time"] = time
            elif checkin["log_type"] == "OUT":
                if employee_checkin_dict[emp_id]["OUT_time"] is None or time > employee_checkin_dict[emp_id]["OUT_time"]:
                    employee_checkin_dict[emp_id]["OUT_time"] = time

        # Calculate work duration, overtime, and short time
        for emp_id, record in employee_checkin_dict.items():
            in_time = record["IN_time"]
            out_time = record["OUT_time"]
            shift_start = record["shift_start"]
            shift_end = record["shift_end"]

            if in_time and out_time:
                actual_work_duration = out_time - in_time
                expected_work_duration = shift_end - shift_start

                # Calculate overtime & shortfall
                if actual_work_duration > expected_work_duration:
                    record["overtime_hours"] = round(actual_work_duration.total_seconds() / 3600 - expected_work_duration.total_seconds() / 3600, 2)
                    record["shortfall_hours"] = 0.0
                elif actual_work_duration < expected_work_duration:
                    record["shortfall_hours"] = round(expected_work_duration.total_seconds() / 3600 - actual_work_duration.total_seconds() / 3600, 2)
                    record["overtime_hours"] = 0.0

        return {"status": "success", "data": list(employee_checkin_dict.values())}

    except Exception as e:
        frappe.log_error(f"Error in get_employee_checkins: {str(e)}", "Employee Checkin API")
        return {"status": "error", "message": _("Something went wrong"), "error": str(e)}
