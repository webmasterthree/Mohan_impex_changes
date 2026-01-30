import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters or {})
	return columns, data


def get_columns():
	return [
		{
			"label": _("Employee ID"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120,
		},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
		{"label": _("Total Absents"), "fieldname": "total_absents", "fieldtype": "Int", "width": 120},
		{
			"label": _("Sandwich Absents"),
			"fieldname": "sandwich_absents",
			"fieldtype": "Int",
			"width": 140,
		},
	]


def get_data(filters=None):
	filters = filters or {}

	conditions = []
	sql_filters = {}

	if filters.get("employee"):
		conditions.append("a.employee = %(employee)s")
		sql_filters["employee"] = filters["employee"]

	# Optional date range filters (recommended)
	if filters.get("from_date"):
		conditions.append("a.attendance_date >= %(from_date)s")
		sql_filters["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("a.attendance_date <= %(to_date)s")
		sql_filters["to_date"] = filters["to_date"]

	condition_sql = (" AND " + " AND ".join(conditions)) if conditions else ""

	# Sandwich rule implemented as:
	# Holiday/Weekly Off date H is counted as "sandwich absent" if:
	# Attendance on previous working day = 'Absent' AND Attendance on next working day = 'Absent'
	# For simplicity, we treat any holiday in employee's holiday list as the middle day.
	#
	# NOTE: Weekly Offs are normally stored as Holiday rows too in Holiday List,
	# so this works for both Holidays + Weekly Offs.

	return frappe.db.sql(
		f"""
		WITH att AS (
			SELECT employee, attendance_date, status
			FROM `tabAttendance`
			WHERE docstatus = 1
		),
		hol AS (
			SELECT hl.parent AS holiday_list, hl.holiday_date
			FROM `tabHoliday` hl
		),
		emp AS (
			SELECT name AS employee, employee_name, holiday_list
			FROM `tabEmployee`
		),
		-- find previous working day (non-holiday) for each holiday date per employee
		prev_work AS (
			SELECT
				e.employee,
				h.holiday_date,
				MAX(a.attendance_date) AS prev_date
			FROM emp e
			JOIN hol h ON h.holiday_list = e.holiday_list
			JOIN att a ON a.employee = e.employee
			LEFT JOIN hol hx
				ON hx.holiday_list = e.holiday_list AND hx.holiday_date = a.attendance_date
			WHERE hx.holiday_date IS NULL
				AND a.attendance_date < h.holiday_date
			GROUP BY e.employee, h.holiday_date
		),
		-- find next working day (non-holiday) for each holiday date per employee
		next_work AS (
			SELECT
				e.employee,
				h.holiday_date,
				MIN(a.attendance_date) AS next_date
			FROM emp e
			JOIN hol h ON h.holiday_list = e.holiday_list
			JOIN att a ON a.employee = e.employee
			LEFT JOIN hol hx
				ON hx.holiday_list = e.holiday_list AND hx.holiday_date = a.attendance_date
			WHERE hx.holiday_date IS NULL
				AND a.attendance_date > h.holiday_date
			GROUP BY e.employee, h.holiday_date
		),
		sandwich AS (
			SELECT
				e.employee,
				e.employee_name,
				COUNT(*) AS sandwich_absents
			FROM emp e
			JOIN hol h ON h.holiday_list = e.holiday_list
			JOIN prev_work pw ON pw.employee = e.employee AND pw.holiday_date = h.holiday_date
			JOIN next_work nw ON nw.employee = e.employee AND nw.holiday_date = h.holiday_date
			JOIN att ap ON ap.employee = e.employee AND ap.attendance_date = pw.prev_date AND ap.status = 'Absent'
			JOIN att an ON an.employee = e.employee AND an.attendance_date = nw.next_date AND an.status = 'Absent'
			GROUP BY e.employee, e.employee_name
		)
		SELECT
			a.employee,
			MAX(a.employee_name) AS employee_name,
			SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS total_absents,
			COALESCE(s.sandwich_absents, 0) AS sandwich_absents
		FROM `tabAttendance` a
		LEFT JOIN sandwich s ON s.employee = a.employee
		WHERE
			a.docstatus = 1
			{condition_sql}
		GROUP BY a.employee
		""",
		sql_filters,
		as_dict=1,
	)
