import frappe

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
