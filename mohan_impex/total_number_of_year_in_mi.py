import frappe
import calendar
from frappe.utils import getdate, today

@frappe.whitelist()
def update_employee_tenure():
    today_date = getdate(today())

    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "date_of_joining"]
    )

    for e in employees:
        if not e.date_of_joining:
            continue

        start_date = getdate(e.date_of_joining)
        end_date = today_date

        years = end_date.year - start_date.year
        months = end_date.month - start_date.month
        days = end_date.day - start_date.day

        if days < 0:
            prev_month = end_date.month - 1 or 12
            prev_year = end_date.year - 1 if end_date.month == 1 else end_date.year
            days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
            days += days_in_prev_month
            months -= 1

        if months < 0:
            months += 12
            years -= 1

        value = f"{years} yr, {months} month, {days} days"

        frappe.db.set_value(
            "Employee",
            e.name,
            "custom__total_number_of_year_in_mi",
            value
        )

    frappe.db.commit()

update_employee_tenure()
