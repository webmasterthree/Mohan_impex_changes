# import frappe
# from frappe.utils import getdate, add_days, formatdate

# @frappe.whitelist()
# def get_employee_attendance_report(start_date=None, end_date=None):
#     """
#     Fetches employee attendance details for a given date range, including:
#     - Shift details
#     - Check-in/Check-out times
#     - Leave type (Sick Leave, Casual Leave, etc.)
#     - Work From Home (WFH)
#     - Holiday details (e.g., Festival, National Holiday)
#     """

#     try:
#         if not start_date or not end_date:
#             return {"status": "error", "message": "Please provide both start_date and end_date."}

#         start_date = getdate(start_date)
#         end_date = getdate(end_date)

#         if start_date > end_date:
#             return {"status": "error", "message": "Start Date cannot be greater than End Date."}

#         # Fetch Employees
#         employees = frappe.db.get_all("Employee", fields=["name", "employee_name", "department", "branch", "reports_to", "company", "holiday_list"])

#         # Initialize Attendance Summary (Daily Format)
#         attendance_summary = {emp["name"]: {
#             "Employee ID": emp["name"],
#             "Employee Name": emp["employee_name"],
#             "Department": emp["department"],
#             "Branch": emp["branch"] if emp["branch"] else "",
#             "Reports To": emp["reports_to"] if emp["reports_to"] else "",
#             "Company": emp["company"]
#         } for emp in employees}

#         # Preload Leave, WFH, and Holidays
#         leaves = frappe.db.get_all(
#             "Leave Application",
#             filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
#             fields=["employee", "from_date", "to_date", "leave_type"]
#         )

#         wfh_records = frappe.db.get_all(
#             "Work From Home",
#             filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
#             fields=["employee", "from_date", "to_date"]
#         )

#         # Fetch Holidays in Bulk
#         holiday_records = frappe.db.sql("""
#             SELECT parent AS employee, holiday_date, description 
#             FROM `tabHoliday`
#             WHERE holiday_date BETWEEN %s AND %s
#         """, (start_date, end_date), as_dict=True)

#         holiday_map = {}
#         for record in holiday_records:
#             holiday_map.setdefault(record["employee"], {})[record["holiday_date"]] = record["description"]

#         # Process each date in the range
#         current_date = start_date
#         while current_date <= end_date:
#             date_str = current_date.strftime("%Y-%m-%d")  # Ensures correct date formatting

#             # Fetch Check-ins for the date
#             checkins = frappe.db.sql("""
#                 SELECT employee, 
#                        MIN(CASE WHEN log_type = 'IN' THEN time END) AS in_time, 
#                        MAX(CASE WHEN log_type = 'OUT' THEN time END) AS out_time
#                 FROM `tabEmployee Checkin`
#                 WHERE DATE(time) = %s
#                 GROUP BY employee
#             """, (current_date,), as_dict=True)

#             checkin_map = {chk["employee"]: chk for chk in checkins}

#             # Assign attendance summary
#             for emp in employees:
#                 emp_id = emp["name"]

#                 # Identify leave type if applicable
#                 leave_type = next((leave["leave_type"] for leave in leaves if leave["employee"] == emp_id and leave["from_date"] <= current_date <= leave["to_date"]), None)
#                 on_wfh = any(wfh["employee"] == emp_id and wfh["from_date"] <= current_date <= wfh["to_date"] for wfh in wfh_records)
#                 holiday_description = holiday_map.get(emp_id, {}).get(current_date, None)
#                 is_sunday = current_date.weekday() == 6

#                 if emp_id in checkin_map and checkin_map[emp_id]["in_time"]:
#                     attendance_summary[emp_id][date_str] = "Present"
#                 elif on_wfh:
#                     attendance_summary[emp_id][date_str] = "WFH"
#                 elif leave_type:
#                     attendance_summary[emp_id][date_str] = leave_type  # Store leave type instead of generic "Leave"
#                 elif holiday_description:
#                     attendance_summary[emp_id][date_str] = f"Holiday - {holiday_description}"
#                 elif is_sunday:
#                     attendance_summary[emp_id][date_str] = "Weekly Off"
#                 else:
#                     attendance_summary[emp_id][date_str] = "Absent"

#             current_date = add_days(current_date, 1)

#         # Add Summary Counts
#         for emp in attendance_summary.values():
#             summary_counts = {
#                 "Present": 0,
#                 "Absent": 0,
#                 "WFH": 0,
#                 "Weekly Off": 0
#             }

#             for status in list(emp.values())[6:]:  # Skip Employee details columns
#                 if status == "Present":
#                     summary_counts["Present"] += 1
#                 elif status == "Absent":
#                     summary_counts["Absent"] += 1
#                 elif status == "WFH":
#                     summary_counts["WFH"] += 1
#                 elif status == "Weekly Off":
#                     summary_counts["Weekly Off"] += 1

#             emp["Summary"] = f"T_P = {summary_counts['Present']}, T_A = {summary_counts['Absent']}, " \
#                              f"T_WFH = {summary_counts['WFH']}, T_WO = {summary_counts['Weekly Off']}"

#         return {"status": "success", "data": list(attendance_summary.values())}

#     except Exception as e:
#         frappe.log_error(f"Error in get_employee_attendance_report: {str(e)}", "Monthly Attendance Report API")
#         return {"status": "error", "message": str(e)}


import frappe
from frappe.utils import getdate, add_days, formatdate

@frappe.whitelist()
def get_employee_attendance_report(start_date=None, end_date=None):
    """
    Fetches employee attendance details for a given date range, including:
    - Shift details
    - Check-in/Check-out times
    - Leave type (Sick Leave, Casual Leave, etc.)
    - Work From Home (WFH)
    - Holiday details (e.g., Festival, National Holiday)
    - Weekly Off (Sunday)
    - Total leave days
    """

    try:
        if not start_date or not end_date:
            return {"status": "error", "message": "Please provide both start_date and end_date."}

        start_date = getdate(start_date)
        end_date = getdate(end_date)

        if start_date > end_date:
            return {"status": "error", "message": "Start Date cannot be greater than End Date."}

        # Fetch Employees
        employees = frappe.db.get_all("Employee", fields=["name", "employee_name", "department", "branch", "reports_to", "company", "holiday_list"])

        # Initialize Attendance Summary (Daily Format)
        attendance_summary = {emp["name"]: {
            "Employee ID": emp["name"],
            "Employee Name": emp["employee_name"],
            "Department": emp["department"],
            "Branch": emp["branch"] if emp["branch"] else "",
            "Reports To": emp["reports_to"] if emp["reports_to"] else "",
            "Company": emp["company"]
        } for emp in employees}

        # Preload Leave, WFH, and Holidays
        leaves = frappe.db.get_all(
            "Leave Application",
            filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "from_date", "to_date", "leave_type"]
        )

        wfh_records = frappe.db.get_all(
            "Work From Home",
            filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "from_date", "to_date"]
        )

        # Fetch Holidays in Bulk
        holiday_records = frappe.db.sql("""
            SELECT parent AS employee, holiday_date, description 
            FROM `tabHoliday`
            WHERE holiday_date BETWEEN %s AND %s
        """, (start_date, end_date), as_dict=True)

        holiday_map = {}
        for record in holiday_records:
            holiday_map.setdefault(record["employee"], {})[record["holiday_date"]] = record["description"]

        # Process each date in the range
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")  # Ensures correct date formatting

            # Fetch Check-ins for the date
            checkins = frappe.db.sql("""
                SELECT employee, 
                       MIN(CASE WHEN log_type = 'IN' THEN time END) AS in_time, 
                       MAX(CASE WHEN log_type = 'OUT' THEN time END) AS out_time
                FROM `tabEmployee Checkin`
                WHERE DATE(time) = %s
                GROUP BY employee
            """, (current_date,), as_dict=True)

            checkin_map = {chk["employee"]: chk for chk in checkins}

            # Assign attendance summary
            for emp in employees:
                emp_id = emp["name"]

                # Identify leave type if applicable
                leave_type = next((leave["leave_type"] for leave in leaves if leave["employee"] == emp_id and leave["from_date"] <= current_date <= leave["to_date"]), None)
                on_wfh = any(wfh["employee"] == emp_id and wfh["from_date"] <= current_date <= wfh["to_date"] for wfh in wfh_records)
                holiday_description = holiday_map.get(emp_id, {}).get(current_date, None)
                is_sunday = current_date.weekday() == 6

                if emp_id in checkin_map and checkin_map[emp_id]["in_time"]:
                    attendance_summary[emp_id][date_str] = "Present"
                elif on_wfh:
                    attendance_summary[emp_id][date_str] = "WFH"
                elif leave_type:
                    attendance_summary[emp_id][date_str] = leave_type  # Store leave type instead of generic "Leave"
                elif holiday_description:
                    attendance_summary[emp_id][date_str] = f"Holiday - {holiday_description}"
                elif is_sunday:
                    attendance_summary[emp_id][date_str] = "Weekly Off"
                else:
                    attendance_summary[emp_id][date_str] = "Absent"

            current_date = add_days(current_date, 1)

        # Add Summary Counts
        for emp in attendance_summary.values():
            summary_counts = {
                "Present": 0,
                "Absent": 0,
                "WFH": 0,
                "Weekly Off": 0,
                "Total Leave": 0
            }

            for status in list(emp.values())[6:]:  # Skip Employee details columns
                if status == "Present":
                    summary_counts["Present"] += 1
                elif status == "Absent":
                    summary_counts["Absent"] += 1
                elif status == "WFH":
                    summary_counts["WFH"] += 1
                elif status == "Weekly Off":
                    summary_counts["Weekly Off"] += 1
                elif "Leave" in status or "Sick Leave" in status or "Casual Leave" in status or "Maternity Leave" in status:
                    summary_counts["Total Leave"] += 1  # Count leave days

            emp["Summary"] = f"T_P = {summary_counts['Present']}, T_A = {summary_counts['Absent']}, " \
                             f"T_WFH = {summary_counts['WFH']}, T_WO = {summary_counts['Weekly Off']}, " \
                             f"T_L = {summary_counts['Total Leave']}"

        return {"status": "success", "data": list(attendance_summary.values())}

    except Exception as e:
        frappe.log_error(f"Error in get_employee_attendance_report: {str(e)}", "Monthly Attendance Report API")
        return {"status": "error", "message": str(e)}
