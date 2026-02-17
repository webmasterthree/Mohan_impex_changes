import frappe
from frappe.utils import nowdate, get_datetime, now_datetime, get_first_day, get_last_day, today, now,getdate
from frappe import _
from datetime import timedelta
from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on

# def before_save_employee_checkin(doc, method=None):
#     """Before saving Employee Checkin, check monthly late count and create Leave Application if necessary."""
#     if doc.log_type == "IN":
#         # Get current month's late check-in count
#         late_checkins = get_employee_late_checkins(doc.employee)
#         print("----late_checkins----",late_checkins)
#         frappe.logger().info(f"[Monthly] Employee {doc.employee} has {late_checkins} late check-ins in current month.")
#         # print("------------------",late_checkins)
#         # Proceed if late check-ins hit a multiple of 3
#         if late_checkins % 3 == 0 and late_checkins > 0:
#             frappe.msgprint(_("Late check-ins reached a multiple of 3 this month. Checking leave availability..."))

#             # Leave types in order of deduction
#             leave_priority = ["Casual Leave", "Sick Leave", "Earned Leave", "Leave Without Pay"]

#             for leave_type in leave_priority:
#                 response = create_leave_application(doc.employee, leave_type)
#                 if "Created" in response:
#                     frappe.msgprint(response)
#                     frappe.logger().info(response)
#                     break
#                 elif "already exists" in response:
#                     frappe.msgprint(response)
#                     break
#             else:
#                 frappe.msgprint(_("No available leave types. Check-in allowed without leave deduction."))


# def get_employee_late_checkins(employee):
#     """Fetch late check-in count for a specific employee in the current month."""
#     today_date = get_datetime().date()
#     first_day_of_month = today_date.replace(day=1)

#     checkins = frappe.db.get_all(
#         "Employee Checkin",
#         filters={
#             "log_type": "IN",
#             "employee": employee,
#             "time": ["between", [first_day_of_month, today_date]]
#         },
#         fields=["shift_start", "time"]
#     )

#     late_count = 0
#     for checkin in checkins:
#         if not checkin.get("shift_start") or not checkin.get("time"):
#             continue  # Skip incomplete records

#         shift_start = get_datetime(checkin["shift_start"])
#         checkin_time = get_datetime(checkin["time"])

#         # Consider late if beyond 16 minutes from shift start
#         if checkin_time > (shift_start + timedelta(minutes=16)):
#             late_count += 1

#     return late_count


# def get_leave_balances(employee):
#     leave_types = ["Casual Leave", "Sick Leave", "Earned Leave"]

#     balances = {}

#     for leave_type in leave_types:
#         try:
#             balance = get_leave_balance_on(
#                 employee=employee,
#                 leave_type=leave_type,
#                 date=frappe.utils.nowdate()
#             )
#             balances[leave_type] = balance or 0
#         except Exception:
#             balances[leave_type] = 0
#     # print(balance)
#     return balances

    # leave_balances = frappe.db.sql(
    #     """
    #     SELECT leave_type,
    #     SUM(CASE WHEN transaction_type = 'Leave Allocation' THEN leaves ELSE 0 END) -
    #     SUM(CASE WHEN transaction_type = 'Leave Application' THEN leaves ELSE 0 END) AS leave_balance
    #     FROM `tabLeave Ledger Entry`
    #     WHERE docstatus = 1 AND employee = %s
    #     GROUP BY leave_type
    #     """,
    #     (employee,),
    #     as_dict=True
    # )

    # return {record["leave_type"]: record["leave_balance"] for record in leave_balances}


# @frappe.whitelist()
# def create_leave_application(employee, leave_type):
#     """Creates a Leave Application for the given leave type if available."""
#     leave_balance = get_leave_balances(employee).get(leave_type, 0)
#     print("---------\n\n\n\n\n\n\n\n\n\n\n\n\n\n------------",leave_balance)
#     if leave_balance <= 0:
#         return f"{leave_type} is not available for Employee {employee}."

#     # Prevent duplicate leave application for today
#     existing_leave = frappe.db.exists("Leave Application", {
#         "employee": employee,
#         "leave_type": leave_type,
#         "from_date": nowdate(),
#         "to_date": nowdate(),
#         "status": ["!=", "Rejected"]
#     })

#     if existing_leave:
#         return f"Leave Application already exists for Employee {employee} today."

#     try:
#         leave_doc = frappe.get_doc({
#             "doctype": "Leave Application",
#             "employee": employee,
#             "leave_type": leave_type,
#             "from_date": nowdate(),
#             "to_date": nowdate(),
#             "posting_date": nowdate(),
#             "description": "Auto Leave Deducted due to Monthly 3x Late Check-Ins",
#             "status": "Approved"
#         })
#         leave_doc.insert(ignore_permissions=True)
#         leave_doc.submit()

#         return f"{leave_type} Leave Application Created for Employee: {employee}."
#     except Exception as e:
#         frappe.logger().error(f"Error creating leave application for {employee}: {str(e)}")
#         return "Failed to create Leave Application. Please check logs."

####################################################################################################################################################







import frappe
from frappe.utils import now, today, getdate, add_days, get_datetime, now_datetime
from datetime import datetime, timedelta

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
    shift = frappe.db.sql("""
        SELECT shift_type
        FROM `tabShift Assignment`
        WHERE employee = %s
            AND status = 'Active'
            AND start_date <= %s
            AND (end_date IS NULL OR end_date >= %s)
        ORDER BY start_date DESC
        LIMIT 1
    """, (employee, date, date), as_dict=True)
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
        filters={
            "employee": employee,
            "time": ["between", [first_day, today_date]]
        },
        fields=["log_type", "time"],
        order_by="time asc"
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

        if end_time <= start_time:  # night shift
            if checkin_time.time() < end_time:
                shift_start = datetime.combine(checkin_date - timedelta(days=1), start_time)
                shift_end   = datetime.combine(checkin_date, end_time)
            else:
                shift_start = datetime.combine(checkin_date, start_time)
                shift_end   = datetime.combine(checkin_date + timedelta(days=1), end_time)
        else:  # day shift
            shift_start = datetime.combine(checkin_date, start_time)
            shift_end   = datetime.combine(checkin_date, end_time)

        # Late IN → alag list
        if chk["log_type"] == "IN":
            if checkin_time > shift_start + timedelta(minutes=16):
                late_in_dates.append(checkin_date)
                frappe.logger().debug(f"LATE IN: {employee} on {checkin_date} at {checkin_time.time()}")

        # Early OUT → alag list
        elif chk["log_type"] == "OUT":
            if checkin_time < shift_end - timedelta(minutes=16):
                early_out_dates.append(checkin_date)
                frappe.logger().debug(f"EARLY OUT: {employee} on {checkin_date} at {checkin_time.time()}")

    return late_in_dates, early_out_dates

# ---------- Get next valid working day for leave marking ----------
def get_next_valid_leave_date(employee, start_date):
    from frappe.utils import add_days

    current_date = getdate(start_date)
    max_search = 60

    for i in range(max_search):
        check_date = add_days(current_date, i)

        shift_name = get_shift_for_date(employee, check_date)
        if not shift_name:
            frappe.logger().debug(f"{employee}: No shift on {check_date} – skipping")
            continue

        shift_doc = frappe.get_cached_doc("Shift Type", shift_name)
        holiday_list = shift_doc.holiday_list
        if holiday_list:
            is_holiday = frappe.db.exists("Holiday", {"parent": holiday_list, "holiday_date": check_date})
            if is_holiday:
                frappe.logger().debug(f"{employee}: {check_date} is holiday – skipping")
                continue

        attendance_exists = frappe.db.exists(
            "Attendance",
            {
                "employee": employee,
                "attendance_date": check_date,
                "docstatus": 1
            }
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
                "docstatus": 1
            }
        )
        if leave_exists:
            frappe.logger().debug(f"{employee}: {check_date} has approved leave – skipping")
            continue

        frappe.logger().debug(f"{employee}: valid leave date found = {check_date}")
        return check_date

    frappe.logger().warning(f"[LEAVE DATE] No valid date for {employee} after {start_date}, returning original")
    return current_date


# ---------- Get leave balances (skip 0.5) ----------
def get_leave_balances(employee):
    from frappe.utils import nowdate
    leave_types = ["Casual Leave", "Sick Leave", "Earned Leave"]
    balances = {}
    for lt in leave_types:
        try:
            bal = get_leave_balance_on(employee, lt, nowdate()) or 0
            balances[lt] = bal if bal != 0.5 else 0
        except Exception:
            balances[lt] = 0
    return balances


# ---------- Determine employee's shift type (Day/Night) ----------
def get_employee_shift_type(employee):
    try:
        shift_assignment = frappe.db.sql("""
            SELECT shift_type, start_date, end_date
            FROM `tabShift Assignment`
            WHERE employee = %s
                AND status = 'Active'
                AND start_date <= CURDATE()
                AND (end_date IS NULL OR end_date >= CURDATE())
            ORDER BY start_date DESC
            LIMIT 1
        """, (employee,), as_dict=True)
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
    data = frappe.db.sql("""
        SELECT DISTINCT employee
        FROM `tabShift Assignment`
        WHERE shift_type = %s
            AND status = 'Active'
            AND start_date <= CURDATE()
            AND (end_date IS NULL OR end_date >= CURDATE())
    """, (shift_name,), as_dict=True)
    return [d.employee for d in data]


# ---------- CORE PROCESSING ----------
def process_employee_leave(employee, context_label, return_result=False):
    from frappe.utils import add_days, getdate

    result = {
        "leave_created": False,
        "skipped": False,
        "reason": "",
        "late_in_count": 0,
        "early_out_count": 0,
        "leave_type": "",
        "created_count": 0
    }

    # 1. Get late events SEPARATE
    late_in_dates, early_out_dates = get_employee_late_checkins_with_dates(employee)
    result["late_in_count"] = len(late_in_dates)
    result["early_out_count"] = len(early_out_dates)

    frappe.logger().info(
        f"[{context_label}] {employee}: "
        f"{len(late_in_dates)} late IN: {late_in_dates} | "
        f"{len(early_out_dates)} early OUT: {early_out_dates}"
    )

    # Dono mein se koi bhi 3 se kam ho to skip
    if len(late_in_dates) < 3 and len(early_out_dates) < 3:
        result["skipped"] = True
        result["reason"] = "Less than 3 late IN and less than 3 early OUT events"
        return result if return_result else None

    # 2. Existing auto leaves check
    today = getdate()
    first_day = get_first_day_from_shift(employee)

    existing_auto = frappe.db.get_all(
        "Leave Application",
        filters={
            "employee": employee,
            "from_date": [">=", first_day],
            "description": ["like", "Auto Leave Deducted:%"],
            "docstatus": 1
        },
        fields=["from_date"]
    )
    used_dates = {d.from_date for d in existing_auto}
    frappe.logger().debug(f"{employee} existing auto leaves: {used_dates}")

    # 3. Target dates nikalo
    target_dates = []

    # --- Late IN: already kitni leaves bani hain dekho ---
    existing_late_in = frappe.db.count(
        "Leave Application",
        filters={
            "employee": employee,
            "from_date": [">=", first_day],
            "description": ["like", "%Late IN%"],
            "docstatus": 1
        }
    )
    # Pehle se process hue events skip karo
    already_processed_in = existing_late_in * 3
    late_in_remaining = late_in_dates[already_processed_in:]

    frappe.logger().debug(
        f"{employee}: LATE IN total={len(late_in_dates)}, "
        f"already processed={already_processed_in}, "
        f"remaining={len(late_in_remaining)}"
    )

    for i in range(2, len(late_in_remaining), 3):
        original_date = late_in_remaining[i]
        frappe.logger().debug(
            f"{employee}: LATE IN 3rd event at index {i}, date {original_date}"
        )
        candidate = get_next_valid_leave_date(employee, original_date)
        attempts = 0
        while candidate in used_dates and attempts < 60:
            next_day = add_days(candidate, 1)
            candidate = get_next_valid_leave_date(employee, next_day)
            attempts += 1
        if attempts >= 60:
            frappe.logger().error(
                f"{employee}: LATE IN could not find unique date from {original_date}"
            )
            continue
        target_dates.append((candidate, "Late IN"))
        used_dates.add(candidate)
        frappe.logger().info(f"{employee}: LATE IN leave target {candidate}")

    # --- Early OUT: already kitni leaves bani hain dekho ---
    existing_early_out = frappe.db.count(
        "Leave Application",
        filters={
            "employee": employee,
            "from_date": [">=", first_day],
            "description": ["like", "%Early OUT%"],
            "docstatus": 1
        }
    )
    # Pehle se process hue events skip karo
    already_processed_out = existing_early_out * 3
    early_out_remaining = early_out_dates[already_processed_out:]

    frappe.logger().debug(
        f"{employee}: EARLY OUT total={len(early_out_dates)}, "
        f"already processed={already_processed_out}, "
        f"remaining={len(early_out_remaining)}"
    )

    for i in range(2, len(early_out_remaining), 3):
        original_date = early_out_remaining[i]
        frappe.logger().debug(
            f"{employee}: EARLY OUT 3rd event at index {i}, date {original_date}"
        )
        candidate = get_next_valid_leave_date(employee, original_date)
        attempts = 0
        while candidate in used_dates and attempts < 60:
            next_day = add_days(candidate, 1)
            candidate = get_next_valid_leave_date(employee, next_day)
            attempts += 1
        if attempts >= 60:
            frappe.logger().error(
                f"{employee}: EARLY OUT could not find unique date from {original_date}"
            )
            continue
        target_dates.append((candidate, "Early OUT"))
        used_dates.add(candidate)
        frappe.logger().info(f"{employee}: EARLY OUT leave target {candidate}")

    if not target_dates:
        result["skipped"] = True
        result["reason"] = "No new leave required"
        return result if return_result else None

    frappe.logger().info(f"{employee}: target leave dates: {target_dates}")

    # 4. Get leave balances
    balance = get_leave_balances(employee)

    # 5. Create leaves
    leave_priority = ["Casual Leave", "Sick Leave", "Earned Leave", "Leave Without Pay"]
    created = 0
    try:
        for leave_date, leave_reason in target_dates:
            selected = None
            for lt in leave_priority:
                if lt == "Leave Without Pay":
                    selected = lt
                    break
                elif balance.get(lt, 0) >= 1:
                    selected = lt
                    break
            if not selected:
                selected = "Leave Without Pay"

            doc = frappe.get_doc({
                "doctype": "Leave Application",
                "employee": employee,
                "leave_type": selected,
                "from_date": leave_date,
                "to_date": leave_date,
                "posting_date": today,
                "description": f"Auto Leave Deducted: 3rd {leave_reason} ({context_label})",
                "status": "Approved"
            })
            doc.insert(ignore_permissions=True)
            doc.submit()

            if selected != "Leave Without Pay":
                balance[selected] -= 1

            created += 1
            frappe.logger().info(
                f"{employee}: created {selected} leave on {leave_date} for {leave_reason}"
            )

        result["leave_created"] = True
        result["created_count"] = created
        result["leave_type"] = "Multiple"
    except Exception as e:
        frappe.logger().error(f"{employee} error: {e}")
        result["skipped"] = True
        result["reason"] = f"Error: {e}"
        if created:
            result["leave_created"] = True
            result["created_count"] = created

    return result if return_result else None



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
    shift_list = frappe.get_all("Shift Type", filters={"enable_auto_attendance": "1"}, pluck="name")
    for shift in shift_list:
        doc = frappe.get_cached_doc("Shift Type", shift)
        doc.last_sync_of_checkin = now()
        doc.save()
        doc.process_auto_attendance()


def pending_attendance_status():
    data = frappe.db.sql("""
        SELECT name, in_time, out_time, status
        FROM `tabAttendance`
        WHERE docstatus = 1
    """, as_dict=1)
    for i in data:
        if i['in_time'] and i['out_time'] is None and i['status'] == "Half Day":
            frappe.db.set_value('Attendance', i['name'], 'status', 'Absent')


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
            # ↓ late_count ki jagah late_in_count aur early_out_count
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
    """Call this from console to debug: frappe.call('mohan_impex.leave_deduction.test_employee', {'employee':'Daiyan Alam'})"""
    result = process_employee_leave(employee, "Manual Test", return_result=True)
    frappe.logger().info(f"Test result for {employee}: {result}")
    return result
