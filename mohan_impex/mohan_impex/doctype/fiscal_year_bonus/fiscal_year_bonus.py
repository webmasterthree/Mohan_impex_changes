# Copyright (c) 2026, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class FiscalYearBonus(Document):
	pass





@frappe.whitelist()
def process_bonus_slip(docname):
	doc = frappe.get_doc("Fiscal Year Bonus", docname)

	# Get fiscal year (based on doc.from_date)
	fiscal_year = frappe.db.get_value(
		"Fiscal Year",
		{
			"year_start_date": ["<=", doc.from_date],
			"year_end_date": [">=", doc.from_date]
		},
		["year_start_date", "year_end_date"],
		as_dict=True
	)

	for row in doc.employee_bonus_table:
		slips = frappe.get_all(
			"Salary Slip",
			filters={
				"employee": row.employee,
				"docstatus": 1,
				"start_date": ["between", [doc.from_date, doc.to_date]]
			},
			fields=["name", "custom_bonus_net_pay", "total_working_days"]
		)

		total_bonus_base = 0
		working_days = 0

		for s in slips:
			total_bonus_base += s.custom_bonus_net_pay or 0
			working_days += s.total_working_days or 0   # ✅ FIXED (sum)

		bonus_percentage = frappe.db.get_single_value(
			'Mohan Impex Settings', 'bonus_percentage'
		)
		bonus_eligible_days = frappe.db.get_single_value(
			'Mohan Impex Settings', 'bonus_eligible_days'
		)

		# ✅ Year-wise bonus check
		exists = frappe.db.exists(
			"Additional Salary",
			{
				"employee": row.employee,
				"salary_component": "Annual Bonus",
				"payroll_date": [
					"between",
					[fiscal_year.year_start_date, fiscal_year.year_end_date]
				],
				"docstatus": ["!=", 2]
			}
		)

		if exists:
			frappe.logger().info(
				f"Annual Bonus already given this year for {row.employee}"
			)
			continue

		# ✅ Eligibility check
		if working_days >= bonus_eligible_days:

			bonus_amount = (total_bonus_base * bonus_percentage) / 100

			# Extra duplicate safety (same date)
			exists_same_date = frappe.db.exists(
				"Additional Salary",
				{
					"employee": row.employee,
					"salary_component": "Annual Bonus",
					"payroll_date": doc.bonus_date,
					"docstatus": ["!=", 2]
				}
			)

			if exists_same_date:
				frappe.logger().info(
					f"Annual Bonus already exists for {row.employee} on {doc.bonus_date}"
				)
				continue

			# ✅ Create Additional Salary
			crt_bonus = frappe.new_doc('Additional Salary')
			crt_bonus.employee = row.employee
			crt_bonus.payroll_date = doc.bonus_date
			crt_bonus.salary_component = 'Annual Bonus'
			crt_bonus.amount = bonus_amount
			crt_bonus.insert()
			crt_bonus.submit()

			row.employee_bonus_slip = crt_bonus.name

	doc.save()