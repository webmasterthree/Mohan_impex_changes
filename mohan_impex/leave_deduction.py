import frappe
from frappe.utils import nowdate, get_datetime, now_datetime
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
from datetime import datetime, timedelta
from frappe.utils import get_datetime, nowdate, now_datetime
from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on


# ========== COMMON HELPER FUNCTIONS ==========

def get_employee_late_checkins(employee):
    """ 
    Count late check-ins in current month (IN late or OUT early). 
    Max 1 penalty per day.
    """
    today = get_datetime().date()
    first_day = today.replace(day=1)
    
    checkins = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "time": ["between", [first_day, today]]
        },
        fields=["log_type", "shift_start", "shift_end", "time"]
    )
    
    late_days = set()  # to ensure max 1 penalty per day
    
    for chk in checkins:
        if not chk.get("time"):
            continue
            
        checkin_time = get_datetime(chk["time"])
        checkin_date = checkin_time.date()
        
        # Skip if already counted
        if checkin_date in late_days:
            continue
        
        # 🔹 Late IN
        if chk.get("log_type") == "IN" and chk.get("shift_start"):
            shift_start = get_datetime(chk["shift_start"])
            if checkin_time > (shift_start + timedelta(minutes=16)):
                late_days.add(checkin_date)
                continue
        
        # 🔹 Early OUT
        if chk.get("log_type") == "OUT":
            if chk.get("shift_end"):
                shift_end = get_datetime(chk["shift_end"])
            elif chk.get("shift_start"):
                shift_end = get_datetime(chk["shift_start"]) + timedelta(hours=9)
            else:
                continue  # cannot calculate
                
            if checkin_time < (shift_end - timedelta(minutes=16)):
                late_days.add(checkin_date)
    
    return len(late_days)


def get_leave_balances(employee):
    """Get leave balances for employee"""
    leave_types = ["Casual Leave", "Sick Leave", "Earned Leave"]
    balances = {}
    
    for lt in leave_types:
        try:
            balances[lt] = get_leave_balance_on(
                employee=employee, 
                leave_type=lt, 
                date=nowdate()
            ) or 0
        except Exception:
            balances[lt] = 0
    
    return balances


def get_employee_shift_type(employee):
    """Get current shift type (Day/Night) from active Shift Assignment"""
    try:
        shift_assignment = frappe.db.sql("""
            SELECT shift_type, start_date, end_date
            FROM `tabShift Assignment`
            WHERE employee = %s 
                AND status = "Active"
                AND start_date <= CURDATE()
                AND (end_date IS NULL OR end_date >= CURDATE())
            ORDER BY start_date DESC
            LIMIT 1
        """, (employee,), as_dict=True)
        
        if shift_assignment:
            shift_type_name = shift_assignment[0].shift_type
            shift_details = frappe.get_cached_doc("Shift Type", shift_type_name)
            
            if shift_details.start_time:
                start_hour = shift_details.start_time.hour
                # Day shift: 6 AM to 6 PM (6 to 18)
                # Night shift: 6 PM to 6 AM (18 to 6)
                if 6 <= start_hour < 18:
                    return "Day"
                else:
                    return "Night"
        
        return "Day"
    except Exception as e:
        frappe.logger().error(f"Error getting shift type for {employee}: {str(e)}")
        return "Day"


def get_employees_by_shift_type(shift_type):
    """Get all active employees with given shift type (Day/Night)"""
    employees = []
    
    all_employees = frappe.get_all(
        "Employee", 
        filters={"status": "Active"}, 
        fields=["name"]
    )
    
    for emp in all_employees:
        emp_shift_type = get_employee_shift_type(emp.name)
        if emp_shift_type == shift_type:
            employees.append(emp.name)
    
    return employees


def get_employees_by_specific_shift(shift_name):
    """Get all active employees assigned to a specific shift"""
    employees = frappe.db.sql("""
        SELECT DISTINCT employee
        FROM `tabShift Assignment`
        WHERE shift_type = %s
            AND status = "Active"
            AND start_date <= CURDATE()
            AND (end_date IS NULL OR end_date >= CURDATE())
    """, (shift_name,), as_dict=True)
    
    return [emp.employee for emp in employees]


# ========== CORE LEAVE PROCESSING ==========

def process_employee_leave(employee, context_label, return_result=False):
    """
    Core function to process late checkins and create leave
    Used by both scheduler and manual button
    
    Args:
        employee: Employee ID
        context_label: Label for logging (e.g., "Day", "Night", shift name)
        return_result: Return detailed result dict
    """
    result = {
        "leave_created": False,
        "skipped": False,
        "reason": "",
        "late_count": 0,
        "leave_type": ""
    }
    
    # Get late checkins count
    late_checkins = get_employee_late_checkins(employee)
    result["late_count"] = late_checkins
    
    frappe.logger().info(f"[{context_label}] Employee {employee} has {late_checkins} late check-ins this month.")
    
    # Only multiples of 3
    if late_checkins % 3 != 0 or late_checkins <= 0:
        result["skipped"] = True
        result["reason"] = f"{late_checkins} late days (need multiple of 3)"
        return result if return_result else None
    
    # Get leave balances
    balance = get_leave_balances(employee)
    
    # Determine leave type priority
    if balance.get("Casual Leave", 0) > 0:
        leave_type = "Casual Leave"
    elif balance.get("Sick Leave", 0) > 0:
        leave_type = "Sick Leave"
    elif balance.get("Earned Leave", 0) > 0:
        leave_type = "Earned Leave"
    else:
        leave_type = "Leave Without Pay"
    
    result["leave_type"] = leave_type
    
    # Prevent duplicate leave today
    exists = frappe.db.exists("Leave Application", {
        "employee": employee,
        "leave_type": leave_type,
        "from_date": nowdate(),
        "to_date": nowdate(),
        "status": ["!=", "Rejected"]
    })
    
    if exists:
        result["skipped"] = True
        result["reason"] = "Leave already exists for today"
        frappe.logger().info(f"{leave_type} already exists for {employee} today. Skipping.")
        return result if return_result else None
    
    # Create leave application
    try:
        leave_doc = frappe.get_doc({
            "doctype": "Leave Application",
            "employee": employee,
            "leave_type": leave_type,
            "from_date": nowdate(),
            "to_date": nowdate(),
            "posting_date": nowdate(),
            "description": f"Auto Leave Deducted: {late_checkins} late/early check-ins this month ({context_label})",
            "status": "Approved"
        })
        leave_doc.insert(ignore_permissions=True)
        leave_doc.submit()
        
        result["leave_created"] = True
        frappe.logger().info(f"{leave_type} Leave created for Employee {employee} ({context_label})")
        
    except Exception as e:
        result["skipped"] = True
        result["reason"] = f"Error: {str(e)}"
        frappe.logger().error(f"Error creating leave for {employee}: {str(e)}")
    
    return result if return_result else None


# ========== SCHEDULER FUNCTIONS (Day/Night Auto) ==========

@frappe.whitelist()
def auto_employee_checkin_day_shift():
    """Scheduler for Day shift employees - Run at 1 AM"""
    employees = get_employees_by_shift_type("Day")
    
    if not employees:
        frappe.logger().info("[Scheduler-Day] No Day shift employees found")
        return
    
    frappe.logger().info(f"[Scheduler-Day] Processing {len(employees)} Day shift employees")
    
    for emp in employees:
        process_employee_leave(emp, "Scheduler-Day")


@frappe.whitelist()
def auto_employee_checkin_night_shift():
    """Scheduler for Night shift employees - Run at 1 PM"""
    employees = get_employees_by_shift_type("Night")
    
    if not employees:
        frappe.logger().info("[Scheduler-Night] No Night shift employees found")
        return
    
    frappe.logger().info(f"[Scheduler-Night] Processing {len(employees)} Night shift employees")
    
    for emp in employees:
        process_employee_leave(emp, "Scheduler-Night")


@frappe.whitelist()
def auto_employee_checkin():
    """Auto detect shift type based on current time"""
    current_hour = now_datetime().hour
    
    if current_hour == 1:  # 1 AM
        auto_employee_checkin_day_shift()
    elif current_hour == 13:  # 1 PM
        auto_employee_checkin_night_shift()
    else:
        frappe.logger().info(f"[Scheduler] Not a scheduled hour: {current_hour}")


# ========== MANUAL BUTTON TRIGGER (Shift-wise) ==========

@frappe.whitelist()
def process_shift_leave_deduction(shift_name):
    """
    Manual trigger from Shift Type button
    Process leave deduction for all employees in specific shift
    """
    if not shift_name:
        frappe.throw("Shift Type name is required")
    
    # Get all employees assigned to this shift
    employees = get_employees_by_specific_shift(shift_name)
    
    if not employees:
        frappe.msgprint(
            f"No active employees found for shift: {shift_name}",
            title="No Employees",
            indicator="orange"
        )
        return
    
    frappe.logger().info(f"[Manual-Button] Processing {len(employees)} employees for shift: {shift_name}")
    
    # Process each employee
    processed_count = 0
    leave_created_count = 0
    details = []
    
    for emp in employees:
        result = process_employee_leave(emp, f"Shift: {shift_name}", return_result=True)
        processed_count += 1
        
        if result.get("leave_created"):
            leave_created_count += 1
            details.append(f"✓ {emp}: Leave created ({result['leave_type']}) - {result['late_count']} late days")
        elif result.get("skipped"):
            details.append(f"○ {emp}: {result['reason']}")
    
    # Show detailed message
    details_html = "<br>".join(details[:15])  # Show first 15
    if len(details) > 15:
        details_html += f"<br><i>... and {len(details) - 15} more</i>"
    
    message = f"""
        <div style="font-size: 14px;">
            <p><b>Shift:</b> {shift_name}</p>
            <p><b>Total Employees:</b> {len(employees)}</p>
            <p><b>Leaves Created:</b> {leave_created_count}</p>
            <p><b>Skipped:</b> {processed_count - leave_created_count}</p>
            <hr>
            <p><b>Details:</b></p>
            <div style="font-size: 12px; max-height: 300px; overflow-y: auto;">
                {details_html}
            </div>
        </div>
    """
    
    frappe.msgprint(
        message,
        title="Leave Deduction Processed",
        indicator="green" if leave_created_count > 0 else "blue"
    )