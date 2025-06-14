import frappe
from frappe import _
from frappe.utils import getdate, nowdate, format_date
from dateutil.relativedelta import relativedelta

def validate_leave_application(doc, method=None):
    """Validate leave application based on monthly accrual from Leave Ledger Entry"""

    # Monthly accrual rates
    monthly_allocation = {
        "Sick Leave": 0.5,
        "Casual Leave": 0.5,
        "Earned Leave": 1.5
    }

    if doc.leave_type not in monthly_allocation:
        return  # Skip for unsupported leave types

    # 🔍 Get earliest Leave Allocation from Leave Ledger Entry
    allocation_entry = frappe.db.get_all(
        "Leave Ledger Entry",
        filters={
            "employee": doc.employee,
            "leave_type": doc.leave_type,
            "transaction_type": "Leave Allocation",
            "docstatus": 1
        },
        fields=["from_date"],
        order_by="from_date asc",
        limit=1
    )

    if not allocation_entry:
        frappe.throw(_("No Leave Allocation found in Leave Ledger Entry for {0}").format(doc.leave_type))

    from_date = getdate(allocation_entry[0].from_date)
    today = getdate(nowdate())

    # 🧮 Calculate full months from from_date to today (inclusive)
    delta = relativedelta(today, from_date)
    months_passed = delta.years * 12 + delta.months + 1

    # Accrued leave based on monthly policy
    accrued = round(monthly_allocation[doc.leave_type] * months_passed, 1)

    # 📊 Sum used leave from Leave Ledger
    entries = frappe.db.get_all(
        'Leave Ledger Entry',
        fields=["leaves"],
        filters={
            "transaction_type": "Leave Application",
            "employee": doc.employee,
            "leave_type": doc.leave_type,
            "is_expired": 0
        }
    )
    used = abs(sum(entry["leaves"] or 0 for entry in entries))
    remaining = accrued - used

    # ❌ Block if requested exceeds allowed
    if doc.total_leave_days > remaining:
        frappe.throw(_(
            "You are applying for {0} days of {1}, but only {2} days are available "
            "as per monthly accrual policy. Accrued since {3}: {4} days "
            "(based on {5} months). Used: {6} days."
        ).format(
            doc.total_leave_days,
            doc.leave_type,
            remaining,
            format_date(from_date),
            accrued,
            months_passed,
            used
        ))

def on_leave_application_before_save(doc, method):
    validate_leave_application(doc)

# import frappe
# from frappe import _dict
# from collections import defaultdict

# def get_leave_balances():
#     # Fetch only non-expired leave entries
#     entries = frappe.db.get_all(
#         'Leave Ledger Entry',
#         fields=['employee', 'leave_type', 'leaves', 'from_date', 'to_date', 'transaction_type'],
#         filters={
#             'transaction_type': ['in', ['Leave Allocation', 'Leave Encashment', 'Leave Application']],
#             'is_expired': 0
#         }
#     )

#     balances = defaultdict(lambda: defaultdict(float))
#     allocations = defaultdict(lambda: defaultdict(float))
#     applications = defaultdict(lambda: defaultdict(float))
#     alloc_dates = defaultdict(lambda: defaultdict(dict))

#     for entry in entries:
#         emp = entry['employee']
#         ltype = entry['leave_type']
#         val = entry['leaves']

#         balances[emp][ltype] += val

#         if entry['transaction_type'] == 'Leave Allocation':
#             allocations[emp][ltype] += val
#             alloc_dates[emp][ltype] = {
#                 'from_date': entry['from_date'],
#                 'to_date': entry['to_date']
#             }

#         elif entry['transaction_type'] == 'Leave Application':
#             applications[emp][ltype] += abs(val)

#     result = []
#     for emp in balances:
#         row = _dict(employee=emp)
#         for ltype in balances[emp]:
#             row[f'{ltype}_allocated'] = allocations[emp][ltype]
#             row[f'{ltype}_used'] = applications[emp][ltype]
#             row[f'{ltype}_balance'] = balances[emp][ltype]
#             if alloc_dates[emp].get(ltype):
#                 row[f'{ltype}_from'] = alloc_dates[emp][ltype]['from_date']
#                 row[f'{ltype}_to'] = alloc_dates[emp][ltype]['to_date']
#         result.append(row)

#     return result
