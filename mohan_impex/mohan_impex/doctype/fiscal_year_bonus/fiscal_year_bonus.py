# Copyright (c) 2026, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class FiscalYearBonus(Document):
	def validate(doc):
		for row in doc.employee_bonus_table:
			slips = frappe.get_all(
				"Salary Slip",
				filters={
					"employee": row.employee,
					"docstatus": 1,
					"start_date": ["between", [doc.from_date, doc.to_date]]
				},
				fields=["name", "custom_bonus_earnings", "custom_bonus_deductions"]
			)

			total_bonus_base = 0
			total_worked_days = 0

			for s in slips:
				earnings   = s.custom_bonus_earnings   or 0
				deductions = s.custom_bonus_deductions or 0
				total_bonus_base += (earnings - deductions)


			bonus_percentage   = frappe.db.get_single_value('Mohan Impex Settings', 'bonus_percentage')
			bonus_eligible_days = frappe.db.get_single_value('Mohan Impex Settings', 'bonus_eligible_days')

			if total_worked_days < bonus_eligible_days:
				frappe.logger().info(f"{row.employee} is not eligible for bonus")
				continue

			bonus_amount = (total_bonus_base * bonus_percentage) / 100

			# Duplicate check
			exists = frappe.db.exists(
				"Additional Salary",
				{
					"employee": row.employee,
					"salary_component": "Annual Bonus",
					"payroll_date": doc.to_date,
					"docstatus": ["!=", 2]
				}
			)

			if exists:
				frappe.logger().info(
					f"Annual Bonus already exists for {row.employee} on {doc.to_date}"
				)
				continue

			# Additional Salary create
			crt_bonus = frappe.new_doc('Additional Salary')
			crt_bonus.employee         = row.employee
			crt_bonus.payroll_date     = now()
			crt_bonus.salary_component = 'Annual Bonus'
			crt_bonus.amount           = bonus_amount
			crt_bonus.insert()
			crt_bonus.submit()

			row.employee_bonus_slip = crt_bonus.name
		
		doc.save()
