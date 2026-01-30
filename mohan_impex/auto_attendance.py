# apps/mohan_impex/mohan_impex/auto_attendance.py

import frappe


def _attendance_exists(employee: str, attendance_date) -> bool:
	"""
	Check ANY Attendance for employee + date (docstatus < 2).
	Do NOT filter by shift because HRMS duplicate validation blocks even if shift differs/blank.
	"""
	return bool(
		frappe.db.exists(
			"Attendance",
			{
				"employee": employee,
				"attendance_date": attendance_date,
				"docstatus": ("<", 2),
			},
		)
	)


def _is_duplicate_attendance_error(exc: Exception) -> bool:
	# Avoid hard import; detect safely
	return exc.__class__.__name__ == "DuplicateAttendanceError"


def _ensure_hrms_mark_attendance_compat():
	"""
	Patch HRMS mark_attendance_and_link_log so:
	1) It supports both signatures:
	   - old: (logs, status, date, working_hours=None)  [in your system 4th arg is working_hours]
	   - new: (logs, status, date, working_hours, late_entry, early_exit, in_time, out_time, shift)
	2) If Attendance already marked for employee+date -> SKIP.
	3) If HRMS still throws DuplicateAttendanceError -> SKIP (do not crash scheduler).
	"""
	try:
		import hrms.hr.doctype.employee_checkin.employee_checkin as checkin_mod
		import hrms.hr.doctype.shift_type.shift_type as shift_type_mod
	except Exception:
		return

	orig = getattr(checkin_mod, "mark_attendance_and_link_log", None)
	if not orig:
		return

	# Avoid patching repeatedly
	if getattr(orig, "__name__", "") == "mark_attendance_and_link_log_compat":
		return

	def mark_attendance_and_link_log_compat(*args, **kwargs):
		# NEW call style (9 args) from ShiftType.process_auto_attendance()
		if len(args) >= 9:
			logs = args[0]
			status = args[1]
			attendance_date = args[2]
			working_hours = args[3]
			late_entry = args[4]
			early_exit = args[5]
			in_time = args[6]
			out_time = args[7]
			shift = args[8]

			employee = (logs[0] or {}).get("employee") if logs else None
			if employee and _attendance_exists(employee, attendance_date):
				return None  # ✅ already marked -> skip

			try:
				# Try NEW signature first
				return orig(
					logs,
					status,
					attendance_date,
					working_hours,
					late_entry,
					early_exit,
					in_time,
					out_time,
					shift,
				)
			except TypeError:
				# Fallback to OLD signature (3-4 args)
				try:
					# In your HRMS, 4th positional arg = working_hours (NOT shift)
					return orig(logs, status, attendance_date, working_hours)
				except Exception as e:
					if _is_duplicate_attendance_error(e):
						return None
					raise
			except Exception as e:
				if _is_duplicate_attendance_error(e):
					return None
				raise

		# OLD call style (3-4 args) from any other place
		if len(args) >= 3:
			logs = args[0]
			status = args[1]
			attendance_date = args[2]
			employee = (logs[0] or {}).get("employee") if logs else None

			if employee and _attendance_exists(employee, attendance_date):
				return None  # ✅ already marked -> skip

			try:
				return orig(*args, **kwargs)
			except Exception as e:
				if _is_duplicate_attendance_error(e):
					return None
				raise

		# Anything else: passthrough
		return orig(*args, **kwargs)

	mark_attendance_and_link_log_compat.__name__ = "mark_attendance_and_link_log_compat"

	# Patch the function in the employee_checkin module
	checkin_mod.mark_attendance_and_link_log = mark_attendance_and_link_log_compat
	# Patch the already-imported reference in shift_type module (IMPORTANT)
	shift_type_mod.mark_attendance_and_link_log = mark_attendance_and_link_log_compat


@frappe.whitelist()
def process_auto_attendance_for_all_shifts():
	"""
	Scheduled Job method: auto_attendance.process_auto_attendance_for_all_shifts
	"""
	_ensure_hrms_mark_attendance_compat()

	shift_list = frappe.get_all("Shift Type", filters={"enable_auto_attendance": "1"}, pluck="name")
	for shift in shift_list:
		doc = frappe.get_cached_doc("Shift Type", shift)
		doc.process_auto_attendance()
