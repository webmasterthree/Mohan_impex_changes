import frappe
from frappe.utils import getdate

def handle_pf_on_submit(doc, method):
    import math

    # Components to exclude from total_deduction
    exclude_components = [
        "Employees State Insurance Corporation",
        "Provident Fund Employer"
    ]

    # Total of the excluded deduction components
    excluded_amount = sum(
        d.amount for d in doc.deductions if d.salary_component in exclude_components
    )

    if excluded_amount:
        updated_total_deduction = doc.total_deduction - excluded_amount
        updated_net_pay = doc.gross_pay - updated_total_deduction
        rounded_total = round(updated_net_pay)  # Rounding to nearest rupee

        # Update fields directly in the DB
        doc.db_set("total_deduction", updated_total_deduction)
        doc.db_set("net_pay", updated_net_pay)
        doc.db_set("rounded_total", rounded_total)

        frappe.msgprint(
            f"net_pay: ₹{updated_net_pay}"
        )



import frappe
from frappe.model.document import Document

def update_salary_fields(doc):
    base_day = 30
    lop = doc.leave_without_pay or 0
    payment_days = base_day - lop

    doc.total_working_days = base_day
    doc.payment_days = payment_days

    total_earnings = 0
    for row in doc.earnings:
        row.amount = (row.amount / base_day) * payment_days
        total_earnings += row.amount

    doc.gross_pay = total_earnings

    total_deduction = doc.total_deduction or 0
    net_pay = total_earnings - total_deduction
    rounded_total = round(net_pay)

    doc.net_pay = net_pay
    doc.rounded_total = rounded_total

    if rounded_total:
        from mohan_impex.amount_in_word import get_money_in_words
        doc.total_in_words = get_money_in_words(rounded_total)

@frappe.whitelist()
def before_submit(doc, method):
    update_salary_fields(doc)




@frappe.whitelist()
def validate(doc, method):
    ot_calculate(doc)
    calculate_working_holiday(doc)
    create_fiscal_year(doc)




def create_fiscal_year(doc):
    slip_month = getdate(doc.start_date).month
    if slip_month != 10: 
        return
    
    year = getdate(doc.start_date).year
    fy_start = f"{year-1}-04-01"
    fy_end   = f"{year}-03-31"
    slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": doc.employee,
            "docstatus": 1,
            "start_date": ["between", [fy_start, fy_end]]
        },
        fields=["name", "gross_pay", "payment_days", "total_working_days"]
    )

    total_earned_salary = 0
    total_worked_days = 0

    for s in slips:
        # Salary earned already accounts for LOP in ERPNext gross_pay
        total_earned_salary += s.gross_pay

        # Actual worked days
        worked = (s.payment_days or 0)
        total_worked_days += worked

    bonus_percentage = frappe.db.get_single_value('Mohan Impex Settings', 'bonus_percentage')
    bonus_eligible_days = frappe.db.get_single_value('Mohan Impex Settings', 'bonus_eligible_days')
    if total_worked_days < bonus_eligible_days:
        return 0   # Not eligibleeligible
    
    bonus_amount = (total_earned_salary * bonus_percentage) / 100
    
    # 🔹 DUPLICATE CHECK
    exists = frappe.db.exists(
        "Additional Salary",
        {
            "employee": doc.employee,
            "salary_component": "Annual Bonus",
            "payroll_date": doc.end_date,
            "docstatus": ["!=", 2]   # not cancelled
        }
    )

    if exists:
        frappe.logger().info(
            f"Annual Bonus already exists for {doc.employee} on {doc.end_date}"
        )
        return

    # create a new document
    crt_bonus = frappe.new_doc('Additional Salary')
    crt_bonus.employee = doc.employee
    crt_bonus.payroll_date = doc.end_date
    crt_bonus.salary_component = 'Annual Bonus'
    crt_bonus.amount = bonus_amount
    crt_bonus.insert()
    crt_bonus.submit()



def on_trash(doc, method):
    slip_month = getdate(doc.start_date).month
    if slip_month != 10: 
        return
    frappe.db.delete("Additional Salary", {
        "employee": doc.employee,
        "payroll_date": ["between", [doc.start_date, doc.end_date]],
        # "salary_slip": doc.name   # agar tumne link field rakha ho
    })



def calculate_working_holiday(doc):
    """
    Count holidays between start_date & end_date
    where employee is marked Present
    """

    result = frappe.db.sql("""
        SELECT COUNT(DISTINCT a.attendance_date)
        FROM `tabAttendance` a
        INNER JOIN `tabShift Assignment` sa
            ON sa.employee = a.employee
            AND sa.status = 'Active'
        INNER JOIN `tabShift Type` st
            ON st.name = sa.shift_type
        INNER JOIN `tabHoliday List` hl
            ON hl.name = st.holiday_list
        INNER JOIN `tabHoliday` h
            ON h.parent = hl.name
            AND h.holiday_date = a.attendance_date
        WHERE
            a.employee = %s
            AND a.docstatus = 1
            AND a.status = 'Present'
            AND a.attendance_date BETWEEN %s AND %s
    """, (
        doc.employee,
        doc.start_date,
        doc.end_date
    ))

    value = result[0][0] if result else 0
    doc.custom_working_holiday = value


def ot_calculate(doc):
    data = frappe.db.get_value(
        "Overtime",
        {
            "employee": doc.employee,
            "from_date": doc.start_date,
            "to_date": doc.end_date
        },
        "total_hours_amount"
    )
    if data:
        ot_comp = frappe.db.get_single_value('Mohan Impex Settings', 'overtime_component')
        exists = frappe.db.exists(
            "Additional Salary",
            {
                "employee": doc.employee,
                "salary_component": ot_comp,
                "payroll_date": doc.end_date,
                "docstatus": ["!=", 2]   # not cancelled
            }
        )

        if exists:
            return

        # create a new document
        crt_bonus = frappe.new_doc('Additional Salary')
        crt_bonus.employee = doc.employee
        crt_bonus.payroll_date = doc.end_date
        crt_bonus.salary_component = ot_comp
        crt_bonus.amount = data
        crt_bonus.insert()
        crt_bonus.submit()