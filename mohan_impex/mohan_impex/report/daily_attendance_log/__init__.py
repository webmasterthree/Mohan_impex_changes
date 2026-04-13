# import frappe
# from datetime import datetime
# from collections import defaultdict


# # 🔹 Format timedelta → readable
# def format_duration(td):
#     if not td:
#         return None

#     total_seconds = int(td.total_seconds())
#     hours = total_seconds // 3600
#     minutes = (total_seconds % 3600) // 60

#     parts = []

#     if hours > 0:
#         parts.append(f"{hours} hour" + ("s" if hours > 1 else ""))

#     if minutes > 0:
#         parts.append(f"{minutes} min" + ("s" if minutes > 1 else ""))

#     return ", ".join(parts) if parts else "0 mins"


# @frappe.whitelist()
# def daily_attendance_log(from_date=None, to_date=None, employee=None):

#     if not from_date or not to_date:
#         frappe.throw("from_date and to_date are required")

#     from_datetime = f"{from_date} 00:00:00"
#     to_datetime = f"{to_date} 23:59:59"

#     # 🔹 STEP 1: Get ALL Active Employees
#     emp_filters = {"status": "Active"}
#     if employee:
#         emp_filters["name"] = employee

#     employees = frappe.db.get_all(
#         "Employee",
#         filters=emp_filters,
#         fields=[
#             "name", "employee_name", "default_shift",
#             "department", "branch", "reports_to",
#             "custom_reports_two", "company", "holiday_list"
#         ],
#         order_by="name asc"   # ✅ ADDED SORTING AT DB LEVEL
#     )

#     if not employees:
#         return []

#     emp_map = {e["name"]: e for e in employees}
#     employee_list = list(emp_map.keys())

#     # 🔹 STEP 2: Fetch Checkins
#     checkins = frappe.db.get_all(
#         "Employee Checkin",
#         fields=["employee", "log_type", "time", "shift"],
#         filters={
#             "employee": ["in", employee_list],
#             "time": ["between", [from_datetime, to_datetime]]
#         },
#         order_by="employee, time asc"
#     )

#     # 🔹 Group checkins
#     checkin_map = defaultdict(lambda: defaultdict(list))

#     for row in checkins:
#         dt = row["time"].date()
#         checkin_map[row["employee"]][dt].append(row)

#     # 🔹 STEP 3: Attendance Map
#     attendance_data = frappe.db.get_all(
#         "Attendance",
#         fields=["employee", "attendance_date", "status"],
#         filters={
#             "employee": ["in", employee_list],
#             "attendance_date": ["between", [from_date, to_date]],
#             "docstatus": 1
#         }
#     )

#     attendance_map = {
#         (d["employee"], d["attendance_date"]): d["status"]
#         for d in attendance_data
#     }

#     # 🔹 STEP 4: Compensatory Work Map
#     comp_off_data = frappe.db.get_all(
#         "Compensatory Leave Request",
#         fields=["employee", "work_from_date", "work_end_date", "leave_type"],
#         filters={"docstatus": 1}
#     )

#     comp_off_map = {}

#     for row in comp_off_data:
#         current_date = row["work_from_date"]

#         while current_date <= row["work_end_date"]:
#             comp_off_map[(row["employee"], current_date)] = row["leave_type"]
#             current_date = frappe.utils.add_days(current_date, 1)

#     # 🔹 STEP 5: Collect shifts
#     shift_set = set()

#     for row in checkins:
#         if row.get("shift"):
#             shift_set.add(row["shift"])

#     for emp in employees:
#         if emp.get("default_shift"):
#             shift_set.add(emp["default_shift"])

#     # 🔹 Shift timings
#     shift_map = {}
#     if shift_set:
#         shift_data = frappe.db.get_all(
#             "Shift Type",
#             filters={"name": ["in", list(shift_set)]},
#             fields=["name", "start_time", "end_time"]
#         )
#         shift_map = {d["name"]: d for d in shift_data}

#     # 🔹 STEP 6: Holiday Map
#     holiday_map = {}

#     for emp in employees:
#         hl = emp.get("holiday_list")
#         if not hl:
#             continue

#         doc = frappe.get_doc("Holiday List", hl)
#         for h in doc.holidays:
#             status = "Weekly Off" if h.weekly_off else "Holiday"
#             holiday_map[(hl, h.holiday_date)] = status

#     # 🔹 STEP 7: Generate Date Range
#     date_cursor = frappe.utils.getdate(from_date)
#     end_date = frappe.utils.getdate(to_date)

#     all_dates = []
#     while date_cursor <= end_date:
#         all_dates.append(date_cursor)
#         date_cursor = frappe.utils.add_days(date_cursor, 1)

#     # 🔹 STEP 8: Build Final Output (SORTED)
#     final_output = []

#     for emp_id in sorted(emp_map.keys()):   # ✅ SORT APPLIED HERE
#         emp = emp_map[emp_id]

#         emp_obj = {
#             "employee": emp_id,
#             "employee_name": emp.get("employee_name"),
#             "department": emp.get("department"),
#             "branch": emp.get("branch"),
#             "reports_to": emp.get("reports_to"),
#             "custom_reports_two": emp.get("custom_reports_two"),
#             "company": emp.get("company"),
#             "holiday_list": emp.get("holiday_list"),
#             "date": []
#         }

#         for dt in all_dates:

#             logs = checkin_map.get(emp_id, {}).get(dt, [])

#             check_in = None
#             check_out = None
#             shift = None

#             for log in logs:
#                 if log["log_type"] == "IN" and not check_in:
#                     check_in = log["time"]
#                     shift = log.get("shift")
#                 elif log["log_type"] == "OUT":
#                     check_out = log["time"]

#             if not shift:
#                 shift = emp.get("default_shift")

#             shift_info = shift_map.get(shift, {})
#             start_td = shift_info.get("start_time")
#             end_td = shift_info.get("end_time")

#             shift_start_dt = datetime.combine(dt, datetime.min.time()) + start_td if start_td else None
#             shift_end_dt = datetime.combine(dt, datetime.min.time()) + end_td if end_td else None

#             # 🔹 Calculations
#             late_by = None
#             early_by = None
#             total_working_hours = None
#             over_time = None

#             if check_in and shift_start_dt:
#                 diff = check_in - shift_start_dt
#                 if diff.total_seconds() > 0:
#                     late_by = format_duration(diff)

#             if check_out and shift_end_dt:
#                 diff = shift_end_dt - check_out
#                 if diff.total_seconds() > 0:
#                     early_by = format_duration(diff)

#             if check_in and check_out:
#                 working = check_out - check_in
#                 if working.total_seconds() > 0:
#                     total_working_hours = format_duration(working)

#             if check_out and shift_end_dt:
#                 diff = check_out - shift_end_dt
#                 if diff.total_seconds() > 0:
#                     over_time = format_duration(diff)

#             # 🔹 Status Priority
#             status = comp_off_map.get((emp_id, dt))

#             if not status:
#                 status = attendance_map.get((emp_id, dt))

#             if not status:
#                 hl = emp.get("holiday_list")
#                 if hl:
#                     status = holiday_map.get((hl, dt))

#             emp_obj["date"].append({
#                 "date": dt.strftime("%d %b %Y"),
#                 "shift": shift,
#                 "shift_start_time": str(start_td) if start_td else None,
#                 "shift_end_time": str(end_td) if end_td else None,
#                 "check_in": check_in.strftime("%H:%M:%S") if check_in else None,
#                 "check_out": check_out.strftime("%H:%M:%S") if check_out else None,
#                 "late_by": late_by,
#                 "early_by": early_by,
#                 "total_working_hours": total_working_hours,
#                 "over_time": over_time,
#                 "status": status
#             })

#         final_output.append(emp_obj)

#     return final_output


import frappe
from datetime import datetime
from collections import defaultdict


# 🔹 Format timedelta → readable
def format_duration(td):
    if not td:
        return None

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []

    if hours > 0:
        parts.append(f"{hours} hour" + ("s" if hours > 1 else ""))

    if minutes > 0:
        parts.append(f"{minutes} min" + ("s" if minutes > 1 else ""))

    return ", ".join(parts) if parts else "0 mins"


@frappe.whitelist()
def daily_attendance_log(from_date=None, to_date=None, employee=None):

    if not from_date or not to_date:
        frappe.throw("from_date and to_date are required")

    from_datetime = f"{from_date} 00:00:00"
    to_datetime = f"{to_date} 23:59:59"

    # 🔹 STEP 1: Get ALL Active Employees
    emp_filters = {"status": "Active"}
    if employee:
        emp_filters["name"] = employee

    employees = frappe.db.get_all(
        "Employee",
        filters=emp_filters,
        fields=[
            "name", "employee_name", "default_shift",
            "department", "branch", "reports_to",
            "custom_reports_two", "company", "holiday_list"
        ],
        order_by="name asc"
    )

    if not employees:
        return []

    emp_map = {e["name"]: e for e in employees}
    employee_list = list(emp_map.keys())

    # 🔹 STEP 2: Fetch Checkins
    checkins = frappe.db.get_all(
        "Employee Checkin",
        fields=["employee", "log_type", "time", "shift"],
        filters={
            "employee": ["in", employee_list],
            "time": ["between", [from_datetime, to_datetime]]
        },
        order_by="employee, time asc"
    )

    checkin_map = defaultdict(lambda: defaultdict(list))

    for row in checkins:
        dt = row["time"].date()
        checkin_map[row["employee"]][dt].append(row)

    # 🔹 STEP 3: Attendance Map
    attendance_data = frappe.db.get_all(
        "Attendance",
        fields=["employee", "attendance_date", "status"],
        filters={
            "employee": ["in", employee_list],
            "attendance_date": ["between", [from_date, to_date]],
            "docstatus": 1
        }
    )

    attendance_map = {
        (d["employee"], d["attendance_date"]): d["status"]
        for d in attendance_data
    }

    # 🔹 STEP 4: Compensatory Work Map
    comp_off_data = frappe.db.get_all(
        "Compensatory Leave Request",
        fields=["employee", "work_from_date", "work_end_date", "leave_type"],
        filters={"docstatus": 1}
    )

    comp_off_map = {}

    for row in comp_off_data:
        current_date = row["work_from_date"]
        while current_date <= row["work_end_date"]:
            comp_off_map[(row["employee"], current_date)] = row["leave_type"]
            current_date = frappe.utils.add_days(current_date, 1)

    # 🔹 STEP 5: Collect shifts
    shift_set = set()

    for row in checkins:
        if row.get("shift"):
            shift_set.add(row["shift"])

    for emp in employees:
        if emp.get("default_shift"):
            shift_set.add(emp["default_shift"])

    # 🔹 Shift timings
    shift_map = {}
    if shift_set:
        shift_data = frappe.db.get_all(
            "Shift Type",
            filters={"name": ["in", list(shift_set)]},
            fields=["name", "start_time", "end_time"]
        )
        shift_map = {d["name"]: d for d in shift_data}

    # 🔹 STEP 6: Holiday Map
    holiday_map = {}

    for emp in employees:
        hl = emp.get("holiday_list")
        if not hl:
            continue

        doc = frappe.get_doc("Holiday List", hl)
        for h in doc.holidays:
            status = "Weekly Off" if h.weekly_off else "Holiday"
            holiday_map[(hl, h.holiday_date)] = status

    # 🔹 STEP 7: Generate Date Range
    date_cursor = frappe.utils.getdate(from_date)
    end_date = frappe.utils.getdate(to_date)

    all_dates = []
    while date_cursor <= end_date:
        all_dates.append(date_cursor)
        date_cursor = frappe.utils.add_days(date_cursor, 1)

    # 🔹 STEP 8: Build Final Output
    final_output = []

    for emp_id in sorted(emp_map.keys()):
        emp = emp_map[emp_id]

        emp_obj = {
            "employee": emp_id,
            "employee_name": emp.get("employee_name"),
            "department": emp.get("department"),
            "branch": emp.get("branch"),
            "reports_to": emp.get("reports_to"),
            "custom_reports_two": emp.get("custom_reports_two"),
            "company": emp.get("company"),
            "holiday_list": emp.get("holiday_list"),
            "date": []
        }

        for dt in all_dates:

            logs = checkin_map.get(emp_id, {}).get(dt, [])

            check_in = None
            check_out = None
            shift = None

            for log in logs:
                if log["log_type"] == "IN" and not check_in:
                    check_in = log["time"]
                    shift = log.get("shift")
                elif log["log_type"] == "OUT":
                    check_out = log["time"]

            if not shift:
                shift = emp.get("default_shift")

            # ✅ SKIP NIGHT SHIFT
            if shift == "Night Shift":
                continue

            shift_info = shift_map.get(shift, {})
            start_td = shift_info.get("start_time")
            end_td = shift_info.get("end_time")

            shift_start_dt = datetime.combine(dt, datetime.min.time()) + start_td if start_td else None
            shift_end_dt = datetime.combine(dt, datetime.min.time()) + end_td if end_td else None

            # 🔹 Calculations
            late_by = None
            early_by = None
            total_working_hours = None
            over_time = None

            if check_in and shift_start_dt:
                diff = check_in - shift_start_dt
                if diff.total_seconds() > 0:
                    late_by = format_duration(diff)

            if check_out and shift_end_dt:
                diff = shift_end_dt - check_out
                if diff.total_seconds() > 0:
                    early_by = format_duration(diff)

            if check_in and check_out:
                working = check_out - check_in
                if working.total_seconds() > 0:
                    total_working_hours = format_duration(working)

            if check_out and shift_end_dt:
                diff = check_out - shift_end_dt
                if diff.total_seconds() > 0:
                    over_time = format_duration(diff)

            # 🔹 Status Priority
            status = comp_off_map.get((emp_id, dt))

            if not status:
                status = attendance_map.get((emp_id, dt))

            if not status:
                hl = emp.get("holiday_list")
                if hl:
                    status = holiday_map.get((hl, dt))

            emp_obj["date"].append({
                "date": dt.strftime("%d %b %Y"),
                "shift": shift,
                "shift_start_time": str(start_td) if start_td else None,
                "shift_end_time": str(end_td) if end_td else None,
                "check_in": check_in.strftime("%H:%M:%S") if check_in else None,
                "check_out": check_out.strftime("%H:%M:%S") if check_out else None,
                "late_by": late_by,
                "early_by": early_by,
                "total_working_hours": total_working_hours,
                "over_time": over_time,
                "status": status
            })

        final_output.append(emp_obj)

    return final_output