import frappe
from frappe.utils import now, getdate, add_days, get_datetime, now_datetime
from datetime import datetime, timedelta

from mohan_impex.leave_balance import leave_balance as leave_balance_api


# ============================================================
# Helpers
# ============================================================

def _to_time(val):
    if isinstance(val, timedelta):
        total_seconds = int(val.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return datetime.strptime(
            f"{hours:02}:{minutes:02}:{seconds:02}", "%H:%M:%S"
        ).time()
    return val


def _fmt_date(val):
    return getdate(val).strftime("%d-%m-%Y") if val else ""


# ============================================================
# Prevent reuse of same violation set
# ============================================================

def is_trigger_already_used(employee, trigger_date):

    return frappe.db.exists(
        "Leave Application",
        {
            "employee": employee,
            "description": ["like", f"%Trigger Date: {_fmt_date(trigger_date)}%"],
            "docstatus": 1,
        },
    )


# ============================================================
# Shift Utilities
# ============================================================

def get_shift_for_date(employee, date):

    shift = frappe.db.sql(
        """
        SELECT shift_type
        FROM `tabShift Assignment`
        WHERE employee=%s
        AND status='Active'
        AND start_date<=%s
        AND (end_date IS NULL OR end_date >= %s)
        ORDER BY start_date DESC
        LIMIT 1
        """,
        (employee, date, date),
        as_dict=True,
    )

    return shift[0].shift_type if shift else None


def get_shift_date_range(shift_name):

    shift_doc = frappe.get_cached_doc("Shift Type", shift_name)

    start = getdate(shift_doc.process_attendance_after) if shift_doc.process_attendance_after else getdate().replace(day=1)
    end = get_datetime(shift_doc.last_sync_of_checkin).date() if shift_doc.last_sync_of_checkin else getdate()

    return start, end


# ============================================================
# Attendance Analysis
# ============================================================

def get_employee_late_checkins_with_dates(employee):

    today = getdate()
    shift_name = get_shift_for_date(employee, today)

    if not shift_name:
        return {}

    start_date, end_date = get_shift_date_range(shift_name)

    checkins = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "time": ["between", [start_date, end_date]],
        },
        fields=["log_type", "time"],
        order_by="time asc",
    )

    month_data = {}

    for chk in checkins:

        checkin_time = get_datetime(chk["time"])
        checkin_date = checkin_time.date()
        month_key = checkin_date.strftime("%Y-%m")

        if month_key not in month_data:
            month_data[month_key] = {"late_in": [], "early_out": []}

        shift_name_day = get_shift_for_date(employee, checkin_date)
        if not shift_name_day:
            continue

        shift_doc = frappe.get_cached_doc("Shift Type", shift_name_day)

        start_time = _to_time(shift_doc.start_time)
        end_time = _to_time(shift_doc.end_time)

        if not start_time or not end_time:
            continue

        if end_time <= start_time:
            if checkin_time.time() < end_time:
                shift_start = datetime.combine(checkin_date - timedelta(days=1), start_time)
                shift_end = datetime.combine(checkin_date, end_time)
            else:
                shift_start = datetime.combine(checkin_date, start_time)
                shift_end = datetime.combine(checkin_date + timedelta(days=1), end_time)
        else:
            shift_start = datetime.combine(checkin_date, start_time)
            shift_end = datetime.combine(checkin_date, end_time)

        if chk["log_type"] == "IN":
            if checkin_time > shift_start + timedelta(minutes=16):
                if checkin_date not in month_data[month_key]["late_in"]:
                    month_data[month_key]["late_in"].append(checkin_date)

        elif chk["log_type"] == "OUT":
            if checkin_time < shift_end - timedelta(minutes=16):
                if checkin_date not in month_data[month_key]["early_out"]:
                    month_data[month_key]["early_out"].append(checkin_date)

    for month in month_data:
        month_data[month]["late_in"].sort()
        month_data[month]["early_out"].sort()

    return month_data


# ============================================================
# Leave Date Selection
# ============================================================

def get_next_valid_leave_date(employee, start_date):

    for i in range(15):

        check_date = add_days(getdate(start_date), i)

        shift_name = get_shift_for_date(employee, check_date)

        if shift_name:
            shift_doc = frappe.get_cached_doc("Shift Type", shift_name)
            if shift_doc.holiday_list and frappe.db.exists(
                "Holiday",
                {"parent": shift_doc.holiday_list, "holiday_date": check_date},
            ):
                continue

        if frappe.db.exists(
            "Leave Application",
            {
                "employee": employee,
                "from_date": ["<=", check_date],
                "to_date": [">=", check_date],
                "docstatus": 1,
            },
        ):
            continue

        return check_date

    return None


# ============================================================
# Leave Priority
# ============================================================

def get_leave_priority_and_balances(employee):

    res = leave_balance_api(employee) or {}
    rows = res.get("message") or []

    out = []

    for r in rows:
        balance = r.get("Balance")
        unlimited = isinstance(balance, str) and balance.lower() == "unlimited"

        balance_num = None if unlimited else float(balance or 0)

        out.append({
            "leave_type": r.get("Leave Type"),
            "priority": int(r.get("Priority") or 999),
            "balance": balance_num,
            "unlimited": unlimited,
        })

    return sorted(out, key=lambda x: (x["priority"], x["leave_type"]))


def pick_leave_type(priority_rows):

    for r in priority_rows:
        if not r["unlimited"] and (r["balance"] or 0) >= 1:
            return r["leave_type"]

    for r in priority_rows:
        if r["unlimited"]:
            return r["leave_type"]

    return "Leave Without Pay"


def decrement_balance(priority_rows, leave_type):

    for r in priority_rows:
        if r["leave_type"] == leave_type and not r["unlimited"]:
            r["balance"] = max(0, (r["balance"] or 0) - 1)


# ============================================================
# Core Leave Logic
# ============================================================

def process_employee_leave(employee, context_label, return_result=False):

    result = {
        "leave_created": False,
        "created_count": 0,
    }

    month_data = get_employee_late_checkins_with_dates(employee)

    if not month_data:
        return result if return_result else None

    today = getdate()
    priority_rows = get_leave_priority_and_balances(employee)

    created = 0

    for month_key, data in sorted(month_data.items()):

        late_in = data["late_in"]
        early_out = data["early_out"]

        target_dates = []

        for i in range(2, len(late_in), 3):
            trigger = late_in[i]
            violations = late_in[i - 2:i + 1]
            candidate = get_next_valid_leave_date(employee, trigger)
            if candidate:
                target_dates.append((candidate, "Late IN", trigger, violations))

        for i in range(2, len(early_out), 3):
            trigger = early_out[i]
            violations = early_out[i - 2:i + 1]
            candidate = get_next_valid_leave_date(employee, trigger)
            if candidate:
                target_dates.append((candidate, "Early OUT", trigger, violations))

        for leave_date, reason, trigger_date, violations in target_dates:

            if is_trigger_already_used(employee, trigger_date):
                continue

            if frappe.db.exists("Leave Application", {
                "employee": employee,
                "from_date": leave_date,
                "to_date": leave_date,
                "docstatus": ["!=", 2],
            }):
                continue

            leave_type = pick_leave_type(priority_rows)

            violation_str = ", ".join(_fmt_date(d) for d in violations)

            description = (
                f"Auto Leave Deducted | Basis: {reason} | "
                f"{reason} Dates: {violation_str} | "
                f"Trigger Date: {_fmt_date(trigger_date)} | "
                f"Leave Date: {_fmt_date(leave_date)} | "
                f"Context: {context_label}"
            )

            try:
                doc = frappe.get_doc({
                    "doctype": "Leave Application",
                    "employee": employee,
                    "leave_type": leave_type,
                    "from_date": leave_date,
                    "to_date": leave_date,
                    "posting_date": today,
                    "description": description,
                    "status": "Approved",
                })

                doc.insert(ignore_permissions=True)
                if doc.docstatus == 0:
                    doc.submit()

                decrement_balance(priority_rows, leave_type)
                created += 1

            except Exception:
                frappe.log_error(frappe.get_traceback(), "Leave Creation Failed")

    result["leave_created"] = created > 0
    result["created_count"] = created

    return result if return_result else None


# ============================================================
# Shift Type Detection
# ============================================================

def get_employee_shift_type(employee):

    shift_assignment = frappe.db.sql(
        """
        SELECT shift_type
        FROM `tabShift Assignment`
        WHERE employee=%s
        AND status='Active'
        AND start_date <= CURDATE()
        AND (end_date IS NULL OR end_date >= CURDATE())
        ORDER BY start_date DESC
        LIMIT 1
        """,
        (employee,),
        as_dict=True,
    )

    if shift_assignment:
        shift_doc = frappe.get_cached_doc("Shift Type", shift_assignment[0].shift_type)

        if shift_doc.start_time:
            start_time = _to_time(shift_doc.start_time)
            return "Day" if 6 <= start_time.hour < 18 else "Night"

    return "Day"


def get_employees_by_shift_type(shift_type):

    employees = []
    all_emps = frappe.get_all("Employee", filters={"status": "Active"}, pluck="name")

    for emp in all_emps:
        if get_employee_shift_type(emp) == shift_type:
            employees.append(emp)

    return employees


# ============================================================
# Scheduler
# ============================================================

@frappe.whitelist()
def auto_employee_checkin_day_shift():
    for emp in get_employees_by_shift_type("Day"):
        process_employee_leave(emp, "Scheduler-Day")

    update_last_sync_attendance()
    pending_attendance_status()


@frappe.whitelist()
def auto_employee_checkin_night_shift():
    for emp in get_employees_by_shift_type("Night"):
        process_employee_leave(emp, "Scheduler-Night")

    update_last_sync_attendance()
    pending_attendance_status()


@frappe.whitelist()
def auto_employee_checkin():

    hour = now_datetime().hour

    if hour == 1:
        auto_employee_checkin_day_shift()
    elif hour == 13:
        auto_employee_checkin_night_shift()


# ============================================================
# Attendance Sync
# ============================================================

def update_last_sync_attendance():

    shift_list = frappe.get_all(
        "Shift Type",
        filters={"enable_auto_attendance": 1},
        pluck="name",
    )

    for shift in shift_list:
        doc = frappe.get_cached_doc("Shift Type", shift)
        doc.last_sync_of_checkin = now()
        doc.save()
        doc.process_auto_attendance()


def pending_attendance_status():

    data = frappe.db.sql(
        """
        SELECT name,in_time,out_time,status
        FROM `tabAttendance`
        WHERE docstatus=1
        """,
        as_dict=True,
    )

    for i in data:
        if i["in_time"] and i["out_time"] is None and i["status"] == "Half Day":
            frappe.db.set_value("Attendance", i["name"], "status", "Absent")


# ============================================================
# Manual Testing
# ============================================================

@frappe.whitelist()
def test_employee(employee):

    result = process_employee_leave(employee, "Manual Test", True)
    frappe.logger().info(f"Test result {employee}: {result}")

    return result