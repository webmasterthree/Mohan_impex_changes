import frappe
from frappe.utils import getdate, add_days

@frappe.whitelist()
def get_employee_attendance_report(start_date=None, end_date=None):
    """
    Fetches employee attendance details for a given date range, including:
    - Shift details
    - Check-in/Check-out times
    - Leave type (Sick Leave, Casual Leave, etc.)
    - Work From Home (WFH)
    - Holidays (e.g., Sunday, Diwali) from holiday list
    - Summary counts
    """
    try:
        if not start_date or not end_date:
            return {"status": "error", "message": "Please provide both start_date and end_date."}

        start_date = getdate(start_date)
        end_date = getdate(end_date)

        if start_date > end_date:
            return {"status": "error", "message": "Start Date cannot be greater than End Date."}

        # Fetch Employees
        employees = frappe.db.get_all("Employee",filters={"status": "Active"}, fields=["name", "employee_name", "department", "branch", "reports_to", "company", "holiday_list"])

        # Initialize Attendance Summary
        attendance_summary = {
            emp["name"]: {
                "Employee ID": emp["name"],
                "Employee Name": emp["employee_name"],
                "Department": emp["department"],
                "Branch": emp.get("branch", ""),
                "Reports To": emp.get("reports_to", ""),
                "Company": emp["company"]
            } for emp in employees
        }

        # Preload Approved Leaves
        leaves = frappe.db.get_all(
            "Leave Application",
            filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "from_date", "to_date", "leave_type"]
        )

        # Preload Approved WFH
        wfh_records = frappe.db.get_all(
            "Work From Home",
            filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "from_date", "to_date"]
        )

        # Fetch all holidays from all used holiday lists
        holiday_lists = list({emp["holiday_list"] for emp in employees if emp["holiday_list"]})
        holiday_records = frappe.db.get_all(
            "Holiday",
            filters={"parent": ["in", holiday_lists], "holiday_date": ["between", [start_date, end_date]]},
            fields=["parent", "holiday_date", "description"]
        )

        # Map holidays: {holiday_list: {date: description}}
        holiday_map = {}
        for h in holiday_records:
            holiday_map.setdefault(h["parent"], {})[h["holiday_date"]] = h["description"]

        # Process each date in the range
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Fetch Check-ins for the date
            checkins = frappe.db.sql("""
                SELECT employee, 
                       MIN(CASE WHEN log_type = 'IN' THEN time END) AS in_time, 
                       MAX(CASE WHEN log_type = 'OUT' THEN time END) AS out_time
                FROM `tabEmployee Checkin`
                WHERE DATE(time) = %s
                GROUP BY employee
            """, (current_date,), as_dict=True)
            checkin_map = {c["employee"]: c for c in checkins}

            # For each employee, compute status
            for emp in employees:
                emp_id = emp["name"]
                holiday_list = emp["holiday_list"]
                emp_holidays = holiday_map.get(holiday_list, {})

                # Determine if it's a holiday for this employee
                holiday_desc = emp_holidays.get(current_date)

                # Leave type (if any)
                leave_type = next(
                    (l["leave_type"] for l in leaves if l["employee"] == emp_id and l["from_date"] <= current_date <= l["to_date"]),
                    None
                )

                # WFH status
                is_wfh = any(wfh["employee"] == emp_id and wfh["from_date"] <= current_date <= wfh["to_date"] for wfh in wfh_records)

                # Check-in status
                in_time = checkin_map.get(emp_id, {}).get("in_time")

                # ✅ Status Priority: Present → Holiday → WFH → Leave → Absent
                if in_time:
                    attendance_summary[emp_id][date_str] = "Present"
                elif holiday_desc:
                    cleaned_desc = holiday_desc.strip().lower()
                    if cleaned_desc == "sunday":
                        attendance_summary[emp_id][date_str] = "Weekly Off"
                    else:
                        attendance_summary[emp_id][date_str] = holiday_desc.strip()
                elif is_wfh:
                    attendance_summary[emp_id][date_str] = "WFH"
                elif leave_type:
                    attendance_summary[emp_id][date_str] = leave_type
                else:
                    attendance_summary[emp_id][date_str] = "Absent"

            current_date = add_days(current_date, 1)

        # Summary counts
        for emp in attendance_summary.values():
            summary = {
                "Present": 0,
                "Absent": 0,
                "WFH": 0,
                "Weekly Off": 0,
                "Total Leave": 0
            }

            for status in list(emp.values())[6:]:  # Skip employee details
                if status == "Present":
                    summary["Present"] += 1
                elif status == "Absent":
                    summary["Absent"] += 1
                elif status == "WFH":
                    summary["WFH"] += 1
                elif status == "Weekly Off":
                    summary["Weekly Off"] += 1
                elif "Leave" in status or status in ["Sick Leave", "Casual Leave", "Maternity Leave"]:
                    summary["Total Leave"] += 1

            emp["Summary"] = f"T_P = {summary['Present']}, T_A = {summary['Absent']}, " \
                             f"T_WFH = {summary['WFH']}, T_WO = {summary['Weekly Off']}, " \
                             f"T_L = {summary['Total Leave']}"

        return {"status": "success", "data": list(attendance_summary.values())}

    except Exception as e:
        frappe.log_error(f"Error in get_employee_attendance_report: {str(e)}", "Monthly Attendance Report API")
        return {"status": "error", "message": str(e)}
