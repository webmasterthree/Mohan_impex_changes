# import frappe
# from frappe import _
# from frappe.utils import getdate, nowdate, format_date
# from dateutil.relativedelta import relativedelta

# def validate_leave_application(doc, method=None):
#     """Validate leave application based on monthly accrual from Leave Ledger Entry"""

#     # Monthly accrual rates
#     monthly_allocation = {
#         "Sick Leave": 0.5,
#         "Casual Leave": 0.5,
#         "Earned Leave": 1.5
#     }

#     if doc.leave_type not in monthly_allocation:
#         return  # Skip for unsupported leave types

#     # 🔍 Get earliest Leave Allocation from Leave Ledger Entry
#     allocation_entry = frappe.db.get_all(
#         "Leave Ledger Entry",
#         filters={
#             "employee": doc.employee,
#             "leave_type": doc.leave_type,
#             "transaction_type": "Leave Allocation",
#             "docstatus": 1
#         },
#         fields=["from_date"],
#         order_by="from_date asc",
#         limit=1
#     )

#     if not allocation_entry:
#         frappe.throw(_("No Leave Allocation found in Leave Ledger Entry for {0}").format(doc.leave_type))

#     from_date = getdate(allocation_entry[0].from_date)
#     today = getdate(nowdate())

#     # 🧮 Calculate full months from from_date to today (inclusive)
#     delta = relativedelta(today, from_date)
#     months_passed = delta.years * 12 + delta.months + 1

#     # Accrued leave based on monthly policy
#     accrued = round(monthly_allocation[doc.leave_type] * months_passed, 1)

#     # 📊 Sum used leave from Leave Ledger
#     entries = frappe.db.get_all(
#         'Leave Ledger Entry',
#         fields=["leaves"],
#         filters={
#             "transaction_type": "Leave Application",
#             "employee": doc.employee,
#             "leave_type": doc.leave_type,
#             "is_expired": 0
#         }
#     )
#     used = abs(sum(entry["leaves"] or 0 for entry in entries))
#     remaining = accrued - used

#     # ❌ Block if requested exceeds allowed
#     if doc.total_leave_days > remaining:
#         frappe.throw(_(
#             "You are applying for {0} days of {1}, but only {2} days are available "
#             "as per monthly accrual policy. Accrued since {3}: {4} days "
#             "(based on {5} months). Used: {6} days."
#         ).format(
#             doc.total_leave_days,
#             doc.leave_type,
#             remaining,
#             format_date(from_date),
#             accrued,
#             months_passed,
#             used
#         ))

# def on_leave_application_before_save(doc, method):
#     validate_leave_application(doc)

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, format_date
from dateutil.relativedelta import relativedelta


def validate_leave_application(doc, method=None):
	"""
	Validate leave application based on monthly accrual policy.

	- Monthly rate is fetched dynamically from Leave Type.monthly_allocate
	- Carry forward (Leave Allocation.unused_leaves) is INCLUDED in eligibility,
	  but monthly accrual is NOT applied on carry forward.
	- Availed is summed from Leave Ledger Entry (ALL TIME, no date filter), as you asked earlier.
	"""

	# 1) Get monthly rate dynamically from Leave Type
	rate = frappe.db.get_value("Leave Type", doc.leave_type, "monthly_allocate")
	try:
		rate = float(rate or 0)
	except Exception:
		rate = 0.0

	# Skip validation if monthly_allocate not set
	if rate <= 0:
		return

	# 2) Get current year allocation (same logic you used)
	today = getdate(nowdate())
	year_start = getdate(f"{today.year}-01-01")
	year_end = getdate(f"{today.year}-12-31")

	alloc_list = frappe.db.get_all(
		"Leave Allocation",
		fields=["from_date", "to_date", "unused_leaves"],
		filters={
			"employee": doc.employee,
			"leave_type": doc.leave_type,
			"docstatus": 1,
			"from_date": [">=", year_start],
			"to_date": ["<=", year_end],
		},
		order_by="from_date asc",
		limit=1,
	)

	if not alloc_list:
		frappe.throw(_("No Leave Allocation found for {0} in current year.").format(doc.leave_type))

	alloc = alloc_list[0]
	alloc_from = getdate(alloc.from_date)
	alloc_to = getdate(alloc.to_date)

	# Carry forward from previous year (no accrual on this)
	carry_forward = float(alloc.unused_leaves or 0)

	# 3) Accrue within allocation window (this year, up to today)
	start = max(year_start, alloc_from)
	end = min(today, year_end, alloc_to)

	if end < start:
		months_passed = 0
	else:
		delta = relativedelta(end, start)
		months_passed = delta.years * 12 + delta.months + 1  # inclusive

	accrued_this_year = round(rate * months_passed, 1)

	# Eligible = carry forward + accrued this year
	eligible = round(carry_forward + accrued_this_year, 1)

	# 4) Sum used leave from Leave Ledger (ALL TIME; no date filter)
	entries = frappe.db.get_all(
		"Leave Ledger Entry",
		fields=["leaves"],
		filters={
			"transaction_type": "Leave Application",
			"employee": doc.employee,
			"leave_type": doc.leave_type,
			"docstatus": 1,
			"is_expired": 0,
		},
	)
	used = abs(sum((e.leaves or 0) for e in entries))

	remaining = round(eligible - used, 1)

	# 5) Block if requested exceeds remaining
	if (doc.total_leave_days or 0) > remaining:
		frappe.throw(
		_("Eligible days: {0} days").format(remaining)
	)


def on_leave_application_before_save(doc, method=None):
	validate_leave_application(doc, method)
