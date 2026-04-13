import frappe
from frappe.utils import getdate, add_days
from mohan_impex.mohan_impex.report.daily_attendance_log_night import daily_attendance_log


def execute(filters=None):
    if not filters:
        filters = {}

    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw("From Date and To Date are required")

    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data


# 🔹 COLUMNS (Dynamic Date-wise)
def get_columns(filters):

    columns = [
        {"label": "Employee ID", "fieldname": "employee", "width": 140},
        {"label": "Employee Name", "fieldname": "employee_name", "width": 180},
        {"label": "Department", "fieldname": "department", "width": 150},
        {"label": "Branch", "fieldname": "branch", "width": 150},
        {"label": "Reports To", "fieldname": "reports_to", "width": 140},
        {"label": "Reports TWo", "fieldname": "custom_reports_two", "width": 140},
        {"label": "Company", "fieldname": "company", "width": 180},
    ]

    start = getdate(filters.get("from_date"))
    end = getdate(filters.get("to_date"))

    while start <= end:
        columns.append({
            "label": start.strftime("%d-%b-%Y"),
            "fieldname": str(start),
            "width": 120
        })
        start = add_days(start, 1)

    return columns


# 🔹 DATA (Pivot Logic)
def get_data(filters):

    result = daily_attendance_log(
        filters.get("from_date"),
        filters.get("to_date"),
        filters.get("employee")
    )

    data = []

    for emp in result:

        # 🔹 Main Employee Row
        base_row = {
            "employee": emp.get("employee"),
            "employee_name": emp.get("employee_name"),
            "department": emp.get("department"),
            "branch": emp.get("branch"),
            "reports_to": emp.get("reports_to"),
            "custom_reports_two":emp.get("custom_reports_two"),
            "company": emp.get("company"),
        }

        data.append(base_row)

        # 🔹 Row Order (INCLUDING SHIFT ROWS)
        row_types = [
            "Shift",
            "Shift Start",
            "Shift End",
            "Check-In",
            "Check-Out",
            "Late By",
            "Early By",
            "Total Hours",
            "Over Time",
            "Status"
        ]

        # 🔹 Initialize Rows
        row_map = {}

        for r in row_types:
            row_map[r] = {
                "employee": r,
                "employee_name": "",
                "department": "",
                "branch": "",
                "reports_to": "",
                "company": ""
            }

        # 🔹 Fill Data
        for d in emp.get("date", []):

            date_key = str(getdate(d["date"]))

            row_map["Shift"][date_key] = d.get("shift") or "-"
            row_map["Shift Start"][date_key] = d.get("shift_start_time") or "-"
            row_map["Shift End"][date_key] = d.get("shift_end_time") or "-"

            row_map["Check-In"][date_key] = d.get("check_in") or "-"
            row_map["Check-Out"][date_key] = d.get("check_out") or "-"
            row_map["Late By"][date_key] = d.get("late_by") or "-"
            row_map["Early By"][date_key] = d.get("early_by") or "-"
            row_map["Total Hours"][date_key] = d.get("total_working_hours") or "-"
            row_map["Over Time"][date_key] = d.get("over_time") or "-"
            row_map["Status"][date_key] = d.get("status") or "-"

        # 🔹 Append Rows in Order
        for r in row_types:
            data.append(row_map[r])

    return data