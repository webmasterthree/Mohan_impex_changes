import frappe
from frappe import _
from frappe.utils import getdate, format_date

def validate_leave_application(doc, method=None):
    """Validate leave application against monthly allocation and past used leaves"""

    # Monthly leave allocation per type
    monthly_allocation = {
        "Sick Leave": 0.5,
        "Casual Leave": 0.5,
        "Earned Leave": 1.5
    }

    if doc.leave_type not in monthly_allocation:
        return

    # Use from_date month or current month
    ref_month = getdate(doc.from_date).month if doc.from_date else getdate().month
    max_allowed = monthly_allocation[doc.leave_type] * ref_month

    # Fetch past used leaves from Leave Ledger Entry
    entries = frappe.db.get_all(
        'Leave Ledger Entry',
        fields=["leaves"],
        filters={
            "transaction_type": "Leave Application",
            "employee": doc.employee,
            "leave_type": doc.leave_type
        }
    )

    # Sum total used leaves (can include negative values due to cancellation)
    used_leaves = sum((entry["leaves"] or 0) for entry in entries)

    # Correct logic: subtract absolute used value from allowed
    remaining_leaves = max_allowed - abs(used_leaves)

    # Check if current application exceeds remaining
    if doc.total_leave_days > remaining_leaves:
        frappe.throw(_(
            "You are applying for {0} days of {1}, but only {2} days are remaining "
            "out of the total {3} days allowed till {4} (Monthly allocation × {5} months). "
            "Used Leaves: {6} days.".format(
                doc.total_leave_days,
                doc.leave_type,
                remaining_leaves,
                max_allowed,
                format_date(doc.from_date) if doc.from_date else "current month",
                ref_month,
                abs(used_leaves)
            )
        ))

def on_leave_application_before_save(doc, method):
    """Executes before saving the document"""
    validate_leave_application(doc)

# import frappe
# from frappe import _
# from frappe.utils import getdate, format_date

# def validate_leave_application(doc, method=None):
#     """Validate leave application against monthly allocation limits"""
#     monthly_allocation = {
#         "Sick Leave": 0.5,
#         "Casual Leave": 0.5,
#         "Earned Leave": 1.5
#     }

#     if doc.leave_type not in monthly_allocation:
#         return

#     # Use leave application's month or current month
#     ref_month = getdate(doc.from_date).month if doc.from_date else getdate().month
#     max_allowed = monthly_allocation[doc.leave_type] * ref_month

#     if doc.total_leave_days > max_allowed:
#         frappe.throw(_(
#             "Cannot allocate {0} days of {1}. Maximum allowed till {2} is {3} days "
#             "(Monthly allocation × {4} months).".format(
#                 doc.total_leave_days,
#                 doc.leave_type,
#                 format_date(doc.from_date) if doc.from_date else "current month",
#                 max_allowed,
#                 ref_month
#             )
#         ))

# def on_leave_application_before_save(doc, method):
#     """Executes before saving the document"""
#     validate_leave_application(doc)



# leave_ledger_entries = frappe.db.get_list('Leave Ledger Entry',
#     fields=["employee", "leave_type", "count(*) as count", "sum(leaves) as total_leaves"],
#     group_by="employee, leave_type"
# )