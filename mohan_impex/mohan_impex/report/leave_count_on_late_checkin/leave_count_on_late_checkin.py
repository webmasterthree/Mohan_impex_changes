# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, get_datetime, today
from datetime import timedelta


def execute(filters=None):
    """
    Script Report: Monthly / Periodic Late Check-in Summary

    Optional filters:
        - from_date (Date)
        - to_date   (Date)
        - employee  (Link: Employee)
    """
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Total Late Check-ins",
            "fieldname": "late_count",
            "fieldtype": "Int",
            "width": 140,
        },
        {
            "label": "Auto Leave Deductions (late // 3)",
            "fieldname": "auto_deductions",
            "fieldtype": "Int",
            "width": 190,
        },
        {
            "label": "First Late Date",
            "fieldname": "first_late_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Last Late Date",
            "fieldname": "last_late_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Lates Until Next Deduction",
            "fieldname": "lates_to_next_deduction",
            "fieldtype": "Int",
            "width": 170,
        },
    ]


def get_data(filters):
    # Resolve date range
    if filters.get("from_date") and filters.get("to_date"):
        from_date = getdate(filters.get("from_date"))
        to_date = getdate(filters.get("to_date"))
    else:
        # Default to current month
        to_date = getdate(today())
        from_date = to_date.replace(day=1)

    employee = filters.get("employee")

    conditions = [
        "ec.log_type = 'IN'",
        "DATE(ec.time) BETWEEN %s AND %s",
        "ec.shift_start IS NOT NULL",
    ]
    values = [from_date, to_date]

    if employee:
        conditions.append("ec.employee = %s")
        values.append(employee)

    query = """
        SELECT
            ec.employee,
            ec.employee_name,
            ec.time,
            ec.shift_start
        FROM `tabEmployee Checkin` ec
        WHERE {conditions}
        ORDER BY ec.employee, ec.time
    """.format(
        conditions=" AND ".join(conditions)
    )

    rows = frappe.db.sql(query, values, as_dict=True)

    # Aggregate late stats per employee
    stats = {}
    grace_minutes = 16

    for row in rows:
        if not row.shift_start or not row.time:
            continue

        shift_start_dt = get_datetime(row.shift_start)
        time_dt = get_datetime(row.time)

        # Late if beyond 16 minutes from shift start
        if time_dt <= (shift_start_dt + timedelta(minutes=grace_minutes)):
            continue

        emp = row.employee
        emp_name = row.employee_name
        checkin_date = getdate(time_dt.date())

        if emp not in stats:
            stats[emp] = {
                "employee": emp,
                "employee_name": emp_name,
                "late_count": 0,
                "first_late_date": checkin_date,
                "last_late_date": checkin_date,
            }

        stats[emp]["late_count"] += 1
        # Update first/last late dates
        if checkin_date < stats[emp]["first_late_date"]:
            stats[emp]["first_late_date"] = checkin_date
        if checkin_date > stats[emp]["last_late_date"]:
            stats[emp]["last_late_date"] = checkin_date

    # Convert stats to report rows
    data = []
    for emp, rec in stats.items():
        late_count = rec["late_count"]
        auto_deductions = late_count // 3
        remainder = late_count % 3
        lates_to_next = 0 if remainder == 0 else 3 - remainder

        data.append(
            {
                "employee": rec["employee"],
                "employee_name": rec["employee_name"],
                "late_count": late_count,
                "auto_deductions": auto_deductions,
                "first_late_date": rec["first_late_date"],
                "last_late_date": rec["last_late_date"],
                "lates_to_next_deduction": lates_to_next,
            }
        )

    return data
