import frappe
from frappe import _
from frappe.utils import now, nowdate, getdate, add_days, get_datetime, now_datetime
from datetime import datetime, timedelta

# ✅ NEW: use your API for priority + balance
from mohan_impex.leave_balance import leave_balance as leave_balance_api


# ---------- Helper: convert time / timedelta to datetime.time ----------
def _to_time(val):
    if isinstance(val, timedelta):
        total_seconds = int(val.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return datetime.strptime(f"{hours:02}:{minutes:02}:{seconds:02}", "%H:%M:%S").time()
    return val


# ---------- Get the shift assignment active on a given date ----------
def get_shift_for_date(employee, date):
    shift = frappe.db.sql(
        """
        SELECT shift_type
        FROM `tabShift Assignment`
        WHERE employee = %s
            AND status = 'Active'
            AND start_date <= %s
            AND (end_date IS NULL OR end_date >= %s)
        ORDER BY start_date DESC
        LIMIT 1
        """,
        (employee, date, date),
        as_dict=True,
    )
    return shift[0].shift_type if shift else None


# ---------- Get process_attendance_after from Shift Type ----------
def get_first_day_from_shift(employee):
    """Return process_attendance_after date from employee's current shift.
    Fallback to current month 1st if not set."""
    today = getdate()
    shift_name = get_shift_for_date(employee, today)
    if shift_name:
        shift_doc = frappe.get_cached_doc("Shift Type", shift_name)
        if shift_doc.process_attendance_after:
            frappe.logger().debug(
                f"{employee}: using process_attendance_after = {shift_doc.process_attendance_after}"
            )
            return getdate(shift_doc.process_attendance_after)

    frappe.logger().debug(f"{employee}: fallback to month start")
    return today.replace(day=1)


# ---------- Get late check-in/early-out dates (with duplicates) ----------
def get_employee_late_checkins_with_dates(employee):
    """Return two separate lists:
    - late_in_dates: dates when employee had late IN
    - early_out_dates: dates when employee had early OUT
    """
    today_date = get_datetime().date()
    first_day = get_first_day_from_shift(employee)

    checkins = frappe.db.get_all(
        "Employee Checkin",
        filters={"employee": employee, "time": ["between", [first_day, today_date]]},
        fields=["log_type", "time"],
        order_by="time asc",
    )

    late_in_dates = []
    early_out_dates = []

    for chk in checkins:
        checkin_time = get_datetime(chk["time"])
        checkin_date = checkin_time.date()

        shift_name = get_shift_for_date(employee, checkin_date)
        if not shift_name:
            continue

        shift_doc = frappe.get_cached_doc("Shift Type", shift_name)
        start_time = _to_time(shift_doc.start_time)
        end_time = _to_time(shift_doc.end_time)
        if not start_time or not end_time:
            continue

        # Night shift handling
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

        # Late IN
        if chk["log_type"] == "IN":
            if checkin_time > shift_start + timedelta(minutes=16):
                late_in_dates.append(checkin_date)
                frappe.logger().debug(
                    f"LATE IN: {employee} on {checkin_date} at {checkin_time.time()}"
                )

        # Early OUT
        elif chk["log_type"] == "OUT":
            if checkin_time < shift_end - timedelta(minutes=16):
                early_out_dates.append(checkin_date)
                frappe.logger().debug(
                    f"EARLY OUT: {employee} on {checkin_date} at {checkin_time.time()}"
                )

    return late_in_dates, early_out_dates


# ---------- Get next valid working day for leave marking ----------
def get_next_valid_leave_date(employee, start_date):
    current_date = getdate(start_date)
    max_search = 60

    original_month = current_date.month
    original_year = current_date.year

    for i in range(max_search):
        check_date = add_days(current_date, i)

        # ✅ Month cross check
        if check_date.month != original_month or check_date.year != original_year:
            frappe.logger().warning(
                f"{employee}: Month cross ho gayi, leave skip for {start_date}"
            )
            return None

        shift_name = get_shift_for_date(employee, check_date)
        if not shift_name:
            frappe.logger().debug(f"{employee}: No shift on {check_date} – skipping")
            continue

        shift_doc = frappe.get_cached_doc("Shift Type", shift_name)
        holiday_list = shift_doc.holiday_list
        if holiday_list:
            is_holiday = frappe.db.exists(
                "Holiday", {"parent": holiday_list, "holiday_date": check_date}
            )
            if is_holiday:
                frappe.logger().debug(f"{employee}: {check_date} is holiday – skipping")
                continue

        attendance_exists = frappe.db.exists(
            "Attendance",
            {"employee": employee, "attendance_date": check_date, "docstatus": ["!=", 2]},
        )
        if attendance_exists:
            frappe.logger().debug(f"{employee}: {check_date} has attendance – skipping")
            continue

        leave_exists = frappe.db.exists(
            "Leave Application",
            {
                "employee": employee,
                "from_date": ["<=", check_date],
                "to_date": [">=", check_date],
                "status": "Approved",
                "docstatus": 1,
            },
        )
        if leave_exists:
            frappe.logger().debug(f"{employee}: {check_date} has approved leave – skipping")
            continue

        frappe.logger().debug(f"{employee}: valid leave date found = {check_date}")
        return check_date

    frappe.logger().warning(
        f"[LEAVE DATE] No valid date for {employee} after {start_date}, returning None"
    )
    return None

# def get_next_valid_leave_date(employee, start_date):
#     current_date = getdate(start_date)
#     max_search = 60

#     for i in range(max_search):
#         check_date = add_days(current_date, i)

#         shift_name = get_shift_for_date(employee, check_date)
#         if not shift_name:
#             frappe.logger().debug(f"{employee}: No shift on {check_date} – skipping")
#             continue

#         shift_doc = frappe.get_cached_doc("Shift Type", shift_name)
#         holiday_list = shift_doc.holiday_list
#         if holiday_list:
#             is_holiday = frappe.db.exists(
#                 "Holiday", {"parent": holiday_list, "holiday_date": check_date}
#             )
#             if is_holiday:
#                 frappe.logger().debug(f"{employee}: {check_date} is holiday – skipping")
#                 continue

#         # ✅ include Draft attendance too (docstatus != 2)
#         attendance_exists = frappe.db.exists(
#             "Attendance",
#             {"employee": employee, "attendance_date": check_date, "docstatus": ["!=", 2]},
#         )
#         if attendance_exists:
#             frappe.logger().debug(f"{employee}: {check_date} has attendance – skipping")
#             continue

#         leave_exists = frappe.db.exists(
#             "Leave Application",
#             {
#                 "employee": employee,
#                 "from_date": ["<=", check_date],
#                 "to_date": [">=", check_date],
#                 "status": "Approved",
#                 "docstatus": 1,
#             },
#         )
#         if leave_exists:
#             frappe.logger().debug(f"{employee}: {check_date} has approved leave – skipping")
#             continue

#         frappe.logger().debug(f"{employee}: valid leave date found = {check_date}")
#         return check_date

#     frappe.logger().warning(
#         f"[LEAVE DATE] No valid date for {employee} after {start_date}, returning original"
#     )
#     return current_date


# ---------- NEW: Priority + Balance from your leave_balance API ----------
def get_leave_priority_and_balances(employee):
    """
    Returns list sorted by Priority:
    [
      {"leave_type": "Casual Leave", "priority": 1, "balance": 1.0, "unlimited": False},
      ...
      {"leave_type": "Leave Without Pay", "priority": 4, "balance": None, "unlimited": True},
    ]
    """
    res = leave_balance_api(employee) or {}
    rows = res.get("message") or []

    out = []
    for r in rows:
        lt = r.get("Leave Type")
        pr = r.get("Priority") or 999
        bal = r.get("Balance")

        unlimited = isinstance(bal, str) and bal.strip().lower() == "unlimited"
        bal_num = None
        if not unlimited:
            try:
                bal_num = float(bal or 0)
                # ✅ keep your old rule: treat 0.5 as 0
                if bal_num == 0.5:
                    bal_num = 0.0
            except Exception:
                bal_num = 0.0

        out.append(
            {
                "leave_type": lt,
                "priority": int(pr) if str(pr).isdigit() else pr,
                "balance": bal_num,
                "unlimited": unlimited,
            }
        )

    out.sort(key=lambda x: (x.get("priority") or 999, x.get("leave_type") or ""))
    return out


def pick_leave_type(priority_rows):
    """
    Picks first leave type in priority order with balance >= 1
    else returns first Unlimited (usually LWP) in that order.
    """
    unlimited_fallback = None
    for r in priority_rows:
        if r.get("unlimited"):
            unlimited_fallback = r["leave_type"]
            continue
        if float(r.get("balance") or 0) >= 1:
            return r["leave_type"]
    return unlimited_fallback or "Leave Without Pay"


def decrement_balance(priority_rows, leave_type):
    """Reduce balance in-memory for same run (skip Unlimited)."""
    for r in priority_rows:
        if r.get("leave_type") == leave_type:
            if r.get("unlimited"):
                return
            r["balance"] = max(0.0, float(r.get("balance") or 0) - 1.0)
            return


# ✅ Optional safety: check if HRMS will count 1 leave day for that date/type
def is_leave_date_eligible(employee, leave_type, d):
    try:
        out = frappe.get_attr(
            "hrms.hr.doctype.leave_application.leave_application.get_number_of_leave_days"
        )(
            employee=employee,
            leave_type=leave_type,
            from_date=d,
            to_date=d,
            half_day=0,
            half_day_date=None,
        )
        days = out.get("leave_days") if isinstance(out, dict) else out
        return float(days or 0) >= 1
    except Exception:
        return False


# ---------- Determine employee's shift type (Day/Night) ----------
def get_employee_shift_type(employee):
    try:
        shift_assignment = frappe.db.sql(
            """
            SELECT shift_type, start_date, end_date
            FROM `tabShift Assignment`
            WHERE employee = %s
                AND status = 'Active'
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
                hour = shift_doc.start_time.hour
                return "Day" if 6 <= hour < 18 else "Night"
        return "Day"
    except Exception as e:
        frappe.logger().error(f"Error in get_employee_shift_type({employee}): {e}")
        return "Day"


def get_employees_by_shift_type(shift_type):
    employees = []
    all_emps = frappe.get_all("Employee", filters={"status": "Active"}, pluck="name")
    for emp in all_emps:
        if get_employee_shift_type(emp) == shift_type:
            employees.append(emp)
    return employees


def get_employees_by_specific_shift(shift_name):
    data = frappe.db.sql(
        """
        SELECT DISTINCT employee
        FROM `tabShift Assignment`
        WHERE shift_type = %s
            AND status = 'Active'
            AND start_date <= CURDATE()
            AND (end_date IS NULL OR end_date >= CURDATE())
        """,
        (shift_name,),
        as_dict=True,
    )
    return [d.employee for d in data]


# ---------- CORE PROCESSING ----------
def process_employee_leave(employee, context_label, return_result=False):
    result = {
        "leave_created": False,
        "skipped": False,
        "reason": "",
        "late_in_count": 0,
        "early_out_count": 0,
        "leave_type": "",
        "created_count": 0,
    }

    late_in_dates, early_out_dates = get_employee_late_checkins_with_dates(employee)
    result["late_in_count"] = len(late_in_dates)
    result["early_out_count"] = len(early_out_dates)

    frappe.logger().info(
        f"[{context_label}] {employee}: "
        f"{len(late_in_dates)} late IN: {late_in_dates} | "
        f"{len(early_out_dates)} early OUT: {early_out_dates}"
    )

    if len(late_in_dates) < 3 and len(early_out_dates) < 3:
        result["skipped"] = True
        result["reason"] = "Less than 3 late IN and less than 3 early OUT events"
        return result if return_result else None

    today_dt = getdate()
    first_day = get_first_day_from_shift(employee)

    existing_auto = frappe.db.get_all(
        "Leave Application",
        filters={
            "employee": employee,
            "from_date": [">=", first_day],
            "description": ["like", "Auto Leave Deducted:%"],
            "docstatus": 1,
        },
        fields=["from_date"],
    )
    used_dates = {d.from_date for d in existing_auto}

    target_dates = []

    # --- Late IN ---
    existing_late_in = frappe.db.count(
        "Leave Application",
        filters={
            "employee": employee,
            "from_date": [">=", first_day],
            "description": ["like", "%Late IN%"],
            "docstatus": 1,
        },
    )
    already_processed_in = existing_late_in * 3
    late_in_remaining = late_in_dates[already_processed_in:]

    for i in range(2, len(late_in_remaining), 3):
        original_date = late_in_remaining[i]
        candidate = get_next_valid_leave_date(employee, original_date)

        # ✅ Month cross ya koi valid date nahi mili
        if candidate is None:
            frappe.logger().warning(
                f"{employee}: LATE IN leave skip - no valid date in same month for {original_date}"
            )
            continue

        attempts = 0
        while candidate in used_dates and attempts < 60:
            candidate = get_next_valid_leave_date(employee, add_days(candidate, 1))
            if candidate is None:
                break
            attempts += 1

        if candidate is None or attempts >= 60:
            frappe.logger().error(
                f"{employee}: LATE IN could not find unique date from {original_date}"
            )
            continue

        target_dates.append((candidate, "Late IN"))
        used_dates.add(candidate)

    # --- Early OUT ---
    existing_early_out = frappe.db.count(
        "Leave Application",
        filters={
            "employee": employee,
            "from_date": [">=", first_day],
            "description": ["like", "%Early OUT%"],
            "docstatus": 1,
        },
    )
    already_processed_out = existing_early_out * 3
    early_out_remaining = early_out_dates[already_processed_out:]

    for i in range(2, len(early_out_remaining), 3):
        original_date = early_out_remaining[i]
        candidate = get_next_valid_leave_date(employee, original_date)

        # ✅ Month cross ya koi valid date nahi mili
        if candidate is None:
            frappe.logger().warning(
                f"{employee}: EARLY OUT leave skip - no valid date in same month for {original_date}"
            )
            continue

        attempts = 0
        while candidate in used_dates and attempts < 60:
            candidate = get_next_valid_leave_date(employee, add_days(candidate, 1))
            if candidate is None:
                break
            attempts += 1

        if candidate is None or attempts >= 60:
            frappe.logger().error(
                f"{employee}: EARLY OUT could not find unique date from {original_date}"
            )
            continue

        target_dates.append((candidate, "Early OUT"))
        used_dates.add(candidate)

    if not target_dates:
        result["skipped"] = True
        result["reason"] = "No new leave required"
        return result if return_result else None

    frappe.logger().info(f"{employee}: target leave dates: {target_dates}")

    priority_rows = get_leave_priority_and_balances(employee)

    created = 0
    try:
        for leave_date, leave_reason in target_dates:
            selected = pick_leave_type(priority_rows)

            candidate = leave_date
            tries = 0
            while tries < 60 and not is_leave_date_eligible(employee, selected, candidate):
                candidate = get_next_valid_leave_date(employee, add_days(candidate, 1))
                if candidate is None:
                    break
                tries += 1

            if candidate is None or tries >= 60:
                frappe.logger().error(
                    f"{employee}: No eligible date found for {selected} from {leave_date} ({leave_reason})"
                )
                continue

            doc = frappe.get_doc(
                {
                    "doctype": "Leave Application",
                    "employee": employee,
                    "leave_type": selected,
                    "from_date": candidate,
                    "to_date": candidate,
                    "posting_date": today_dt,
                    "description": f"Auto Leave Deducted: 3rd {leave_reason} ({context_label})",
                    "status": "Approved",
                }
            )
            doc.insert(ignore_permissions=True)
            doc.submit()

            decrement_balance(priority_rows, selected)

            created += 1
            frappe.logger().info(
                f"{employee}: created {selected} leave on {candidate} for {leave_reason}"
            )

        result["leave_created"] = created > 0
        result["created_count"] = created
        result["leave_type"] = "Multiple" if created > 1 else (selected if created == 1 else "")
        if created == 0:
            result["skipped"] = True
            result["reason"] = "No eligible leave dates found"
    except Exception as e:
        frappe.logger().error(f"{employee} error: {e}")
        result["skipped"] = True
        result["reason"] = f"Error: {e}"
        result["leave_created"] = created > 0
        result["created_count"] = created

    return result if return_result else None

# def process_employee_leave(employee, context_label, return_result=False):
#     result = {
#         "leave_created": False,
#         "skipped": False,
#         "reason": "",
#         "late_in_count": 0,
#         "early_out_count": 0,
#         "leave_type": "",
#         "created_count": 0,
#     }

#     # 1) Get late/early events
#     late_in_dates, early_out_dates = get_employee_late_checkins_with_dates(employee)
#     result["late_in_count"] = len(late_in_dates)
#     result["early_out_count"] = len(early_out_dates)

#     frappe.logger().info(
#         f"[{context_label}] {employee}: "
#         f"{len(late_in_dates)} late IN: {late_in_dates} | "
#         f"{len(early_out_dates)} early OUT: {early_out_dates}"
#     )

#     # If both < 3, skip
#     if len(late_in_dates) < 3 and len(early_out_dates) < 3:
#         result["skipped"] = True
#         result["reason"] = "Less than 3 late IN and less than 3 early OUT events"
#         return result if return_result else None

#     today_dt = getdate()
#     first_day = get_first_day_from_shift(employee)

#     # 2) Existing auto leaves (prevent same date reuse)
#     existing_auto = frappe.db.get_all(
#         "Leave Application",
#         filters={
#             "employee": employee,
#             "from_date": [">=", first_day],
#             "description": ["like", "Auto Leave Deducted:%"],
#             "docstatus": 1,
#         },
#         fields=["from_date"],
#     )
#     used_dates = {d.from_date for d in existing_auto}

#     # 3) Build target dates
#     target_dates = []

#     # --- Late IN processed count ---
#     existing_late_in = frappe.db.count(
#         "Leave Application",
#         filters={
#             "employee": employee,
#             "from_date": [">=", first_day],
#             "description": ["like", "%Late IN%"],
#             "docstatus": 1,
#         },
#     )
#     already_processed_in = existing_late_in * 3
#     late_in_remaining = late_in_dates[already_processed_in:]

#     for i in range(2, len(late_in_remaining), 3):
#         original_date = late_in_remaining[i]
#         candidate = get_next_valid_leave_date(employee, original_date)

#         attempts = 0
#         while candidate in used_dates and attempts < 60:
#             candidate = get_next_valid_leave_date(employee, add_days(candidate, 1))
#             attempts += 1

#         if attempts >= 60:
#             frappe.logger().error(
#                 f"{employee}: LATE IN could not find unique date from {original_date}"
#             )
#             continue

#         target_dates.append((candidate, "Late IN"))
#         used_dates.add(candidate)

#     # --- Early OUT processed count ---
#     existing_early_out = frappe.db.count(
#         "Leave Application",
#         filters={
#             "employee": employee,
#             "from_date": [">=", first_day],
#             "description": ["like", "%Early OUT%"],
#             "docstatus": 1,
#         },
#     )
#     already_processed_out = existing_early_out * 3
#     early_out_remaining = early_out_dates[already_processed_out:]

#     for i in range(2, len(early_out_remaining), 3):
#         original_date = early_out_remaining[i]
#         candidate = get_next_valid_leave_date(employee, original_date)

#         attempts = 0
#         while candidate in used_dates and attempts < 60:
#             candidate = get_next_valid_leave_date(employee, add_days(candidate, 1))
#             attempts += 1

#         if attempts >= 60:
#             frappe.logger().error(
#                 f"{employee}: EARLY OUT could not find unique date from {original_date}"
#             )
#             continue

#         target_dates.append((candidate, "Early OUT"))
#         used_dates.add(candidate)

#     if not target_dates:
#         result["skipped"] = True
#         result["reason"] = "No new leave required"
#         return result if return_result else None

#     frappe.logger().info(f"{employee}: target leave dates: {target_dates}")

#     # 4) NEW: Get priority + balances from API (DB-driven)
#     priority_rows = get_leave_priority_and_balances(employee)

#     # 5) Create leaves
#     created = 0
#     try:
#         for leave_date, leave_reason in target_dates:
#             selected = pick_leave_type(priority_rows)

#             # ✅ Ensure eligible day != 0 (avoid 'Eligible days: 0.0 days')
#             candidate = leave_date
#             tries = 0
#             while tries < 60 and not is_leave_date_eligible(employee, selected, candidate):
#                 candidate = get_next_valid_leave_date(employee, add_days(candidate, 1))
#                 tries += 1

#             if tries >= 60:
#                 frappe.logger().error(
#                     f"{employee}: No eligible date found for {selected} from {leave_date} ({leave_reason})"
#                 )
#                 continue

#             doc = frappe.get_doc(
#                 {
#                     "doctype": "Leave Application",
#                     "employee": employee,
#                     "leave_type": selected,
#                     "from_date": candidate,
#                     "to_date": candidate,
#                     "posting_date": today_dt,
#                     "description": f"Auto Leave Deducted: 3rd {leave_reason} ({context_label})",
#                     "status": "Approved",
#                 }
#             )
#             doc.insert(ignore_permissions=True)
#             doc.submit()

#             # ✅ reduce in-memory balance for next leaves in same run
#             decrement_balance(priority_rows, selected)

#             created += 1
#             frappe.logger().info(
#                 f"{employee}: created {selected} leave on {candidate} for {leave_reason}"
#             )

#         result["leave_created"] = created > 0
#         result["created_count"] = created
#         result["leave_type"] = "Multiple" if created > 1 else (selected if created == 1 else "")
#         if created == 0:
#             result["skipped"] = True
#             result["reason"] = "No eligible leave dates found"
#     except Exception as e:
#         frappe.logger().error(f"{employee} error: {e}")
#         result["skipped"] = True
#         result["reason"] = f"Error: {e}"
#         result["leave_created"] = created > 0
#         result["created_count"] = created

#     return result if return_result else None


# ---------- SCHEDULERS ----------
@frappe.whitelist()
def auto_employee_checkin_day_shift():
    employees = get_employees_by_shift_type("Day")
    if not employees:
        frappe.logger().info("[Scheduler-Day] No Day shift employees")
        return
    frappe.logger().info(f"[Scheduler-Day] Processing {len(employees)} employees")
    for emp in employees:
        process_employee_leave(emp, "Scheduler-Day")
    update_last_sync_attendance()
    pending_attendance_status()


@frappe.whitelist()
def auto_employee_checkin_night_shift():
    employees = get_employees_by_shift_type("Night")
    if not employees:
        frappe.logger().info("[Scheduler-Night] No Night shift employees")
        return
    frappe.logger().info(f"[Scheduler-Night] Processing {len(employees)} employees")
    for emp in employees:
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
    else:
        frappe.logger().info(f"[Scheduler] Not scheduled hour {hour}")


# ---------- ATTENDANCE SYNC HELPERS ----------
def update_last_sync_attendance():
    shift_list = frappe.get_all(
        "Shift Type", filters={"enable_auto_attendance": "1"}, pluck="name"
    )
    for shift in shift_list:
        doc = frappe.get_cached_doc("Shift Type", shift)
        doc.last_sync_of_checkin = now()
        doc.save()
        doc.process_auto_attendance()


def pending_attendance_status():
    data = frappe.db.sql(
        """
        SELECT name, in_time, out_time, status
        FROM `tabAttendance`
        WHERE docstatus = 1
        """,
        as_dict=1,
    )
    for i in data:
        if i["in_time"] and i["out_time"] is None and i["status"] == "Half Day":
            frappe.db.set_value("Attendance", i["name"], "status", "Absent")


# ---------- MANUAL BUTTON (Shift Type) ----------
@frappe.whitelist()
def process_shift_leave_deduction(shift_name):
    if not shift_name:
        frappe.throw("Shift Type name is required")

    employees = get_employees_by_specific_shift(shift_name)
    if not employees:
        frappe.msgprint(f"No active employees found for shift: {shift_name}", indicator="orange")
        return

    processed = 0
    leaves_created = 0
    details = []

    for emp in employees:
        res = process_employee_leave(emp, f"Shift: {shift_name}", return_result=True)
        processed += 1

        if res.get("leave_created"):
            leaves_created += 1
            details.append(
                f"✓ {emp}: Leave created "
                f"(Late IN: {res['late_in_count']} | Early OUT: {res['early_out_count']})"
            )
        elif res.get("skipped"):
            details.append(
                f"○ {emp}: {res['reason']} "
                f"(Late IN: {res['late_in_count']} | Early OUT: {res['early_out_count']})"
            )

    msg = f"""
        <div style="font-size:14px;">
            <p><b>Shift:</b> {shift_name}</p>
            <p><b>Total Employees:</b> {len(employees)}</p>
            <p><b>Leaves Created:</b> {leaves_created}</p>
            <p><b>Skipped:</b> {processed - leaves_created}</p>
            <hr><p><b>Details:</b></p>
            <div style="max-height:300px; overflow-y:auto; font-size:12px;">
                {'<br>'.join(details[:15])}
                {'' if len(details)<=15 else '<br><i>... and more</i>'}
            </div>
        </div>
    """
    frappe.msgprint(msg, title="Leave Deduction Processed", indicator="green" if leaves_created else "blue")


# ---------- MANUAL TEST FUNCTION (call from console) ----------
@frappe.whitelist()
def test_employee(employee):
    """Console:
    from mohan_impex.leave_deduction import test_employee
    test_employee('HR-EMP-00008')
    """
    result = process_employee_leave(employee, "Manual Test", return_result=True)
    frappe.logger().info(f"Test result for {employee}: {result}")
    return result
 
