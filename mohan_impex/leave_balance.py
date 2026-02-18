import frappe
from frappe import _
from frappe.utils import getdate, nowdate
from dateutil.relativedelta import relativedelta


@frappe.whitelist()
def leave_balance(employee):
	today = getdate(nowdate())
	year_start = getdate(f"{today.year}-01-01")
	year_end = getdate(f"{today.year}-12-31")

	leave_types = frappe.db.get_all(
		"Leave Type",
		fields=["name", "monthly_allocate", "priority", "is_lwp"],
		order_by="priority asc, name asc",
	)

	out = []

	for lt in leave_types:
		leave_type = lt.name
		is_lwp = int(lt.get("is_lwp") or 0)

		# Availed (common for all leave types)
		used_entries = frappe.db.get_all(
			"Leave Ledger Entry",
			filters={
				"employee": employee,
				"leave_type": leave_type,
				"transaction_type": "Leave Application",
				"docstatus": 1,
				"is_expired": 0,
			},
			fields=["leaves"],
		)
		availed = abs(sum((e.leaves or 0) for e in used_entries))

		# LWP => Unlimited balance
		if is_lwp == 1:
			out.append(
				{
					"Leave Type": leave_type,
					"Priority": lt.get("priority"),
					"Balance": _("Unlimited"),
				}
			)
			continue

		# Non-LWP leave types => allocation + accrual logic
		try:
			rate = float(lt.get("monthly_allocate") or 0)
		except Exception:
			rate = 0.0

		# If no monthly allocation, skip
		if rate <= 0:
			continue

		alloc_list = frappe.db.get_all(
			"Leave Allocation",
			fields=["unused_leaves", "from_date", "to_date"],
			filters={
				"employee": employee,
				"leave_type": leave_type,
				"docstatus": 1,
				"from_date": [">=", year_start],
				"to_date": ["<=", year_end],
			},
			order_by="from_date asc",
			limit=1,
		)

		# show only if allocation exists for this year
		if not alloc_list:
			continue

		alloc = alloc_list[0]
		alloc_from = getdate(alloc.from_date)
		alloc_to = getdate(alloc.to_date)

		carry_forward = float(alloc.unused_leaves or 0)

		start = max(year_start, alloc_from)
		end = min(today, year_end, alloc_to)

		if end < start:
			months_passed = 0
		else:
			delta = relativedelta(end, start)
			months_passed = delta.years * 12 + delta.months + 1

		accrued_this_year = rate * months_passed
		eligible = carry_forward + accrued_this_year
		balance = eligible - availed

		out.append(
			{
				"Leave Type": leave_type,
				"Priority": lt.get("priority"),
				"Balance": balance,
			}
		)

	return frappe._dict(message=out)
