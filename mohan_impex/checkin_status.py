# import frappe
# from frappe.utils import now_datetime, getdate
# from datetime import datetime, timedelta

# @frappe.whitelist()
# def hours_left_to_checkout(employee):
#     if not employee:
#         return None

#     today = getdate()
#     now_dt = now_datetime()

#     SA = frappe.qb.DocType("Shift Assignment")

#     rows = (
#         frappe.qb.from_(SA)
#         .select(SA.shift_type)
#         .where(
#             (SA.employee == employee)
#             & (SA.docstatus == 1)
#             & (SA.status == "Active")
#             & (SA.start_date <= today)
#             & ((SA.end_date.isnull()) | (SA.end_date == "") | (SA.end_date >= today))
#         )
#         .orderby(SA.start_date, order=frappe.qb.desc)
#         .limit(1)
#     ).run(as_dict=True)

#     if not rows:
#         return None

#     shift_type = rows[0].get("shift_type")
#     if not shift_type:
#         return None

#     start_td = frappe.db.get_value("Shift Type", shift_type, "start_time")
#     end_td = frappe.db.get_value("Shift Type", shift_type, "end_time")
#     delay_hours = frappe.db.get_value("Shift Type", shift_type, "custom_allowed_checkout_delay") or 0

#     if not end_td:
#         return None

#     base_day = today
#     if start_td and end_td < start_td:  # overnight shift
#         base_day = base_day + timedelta(days=1)

#     checkout_deadline = (
#         datetime.combine(base_day, datetime.min.time())
#         + end_td
#         + timedelta(hours=float(delay_hours))
#     )

#     return round((checkout_deadline - now_dt).total_seconds() / 3600, 2)


import frappe
from frappe.utils import now_datetime, getdate
from datetime import datetime, timedelta


@frappe.whitelist()
def checkin_status(employee):
	"""
	Returns:
	{
	  "status": "IN" | "OUT" | None,
	  "next_action": "IN" | "OUT",
	  "label": "Check In" | "Check Out",
	  "last_log_time": datetime | None,
	  "hours_left_to_checkout": float | None   # never negative
	}

	Rule:
	- If status is IN but hours_left_to_checkout == 0, force next_action=IN (Check In)
	"""
	if not employee:
		return {
			"status": None,
			"next_action": "IN",
			"label": "Check In",
			"last_log_time": None,
			"hours_left_to_checkout": None,
		}

	today = getdate()
	now_dt = now_datetime()

	# -----------------------------
	# 1) Hours left to checkout (never negative)
	# -----------------------------
	SA = frappe.qb.DocType("Shift Assignment")

	shift_rows = (
		frappe.qb.from_(SA)
		.select(SA.shift_type)
		.where(
			(SA.employee == employee)
			& (SA.docstatus == 1)
			& (SA.status == "Active")
			& (SA.start_date <= today)
			& ((SA.end_date.isnull()) | (SA.end_date == "") | (SA.end_date >= today))
		)
		.orderby(SA.start_date, order=frappe.qb.desc)
		.limit(1)
	).run(as_dict=True)

	hours_left = None

	if shift_rows:
		shift_type = shift_rows[0].get("shift_type")

		if shift_type:
			start_td = frappe.db.get_value("Shift Type", shift_type, "start_time")
			end_td = frappe.db.get_value("Shift Type", shift_type, "end_time")
			delay_hours = (
				frappe.db.get_value("Shift Type", shift_type, "custom_allowed_checkout_delay") or 0
			)

			if end_td:
				base_day = today
				# overnight shift
				if start_td and end_td < start_td:
					base_day = base_day + timedelta(days=1)

				checkout_deadline = (
					datetime.combine(base_day, datetime.min.time())
					+ end_td
					+ timedelta(hours=float(delay_hours))
				)

				diff_hours = (checkout_deadline - now_dt).total_seconds() / 3600
				hours_left = round(max(diff_hours, 0), 2)

	# -----------------------------
	# 2) Latest Employee Checkin (today) to decide status
	# -----------------------------
	EC = frappe.qb.DocType("Employee Checkin")

	last_log = (
		frappe.qb.from_(EC)
		.select(EC.log_type, EC.time)
		.where((EC.employee == employee) & (EC.time >= today))
		.orderby(EC.time, order=frappe.qb.desc)
		.limit(1)
	).run(as_dict=True)

	status = None
	last_log_time = None

	if last_log:
		status = last_log[0].get("log_type")  # "IN" or "OUT"
		last_log_time = last_log[0].get("time")

	# -----------------------------
	# 3) Next action logic (with your special rule)
	# -----------------------------
	# Default behavior:
	# IN -> OUT, OUT/None -> IN
	if status == "IN":
		next_action = "OUT"
		label = "Check Out"
	else:
		next_action = "IN"
		label = "Check In"

	# Special rule:
	# If currently IN but hours_left_to_checkout is 0 => force Check In
	# (meaning checkout is not allowed anymore / shift expired)
	if status == "IN" and (hours_left is not None) and hours_left <= 0:
		next_action = "IN"
		label = "Check In"

	return {
		"status": status,
		"next_action": next_action,
		"label": label,
		"last_log_time": last_log_time,
		"hours_left_to_checkout": hours_left,
	}