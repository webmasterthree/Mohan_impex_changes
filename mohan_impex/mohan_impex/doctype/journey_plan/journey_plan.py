# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import datetime
import frappe

class JourneyPlan(Document):
	def before_save(self):
		range_exists = frappe.db.exists("Journey Plan", {"visit_from_date": ["<=", self.visit_to_date], "visit_to_date": [">=", self.visit_from_date]})
		if range_exists:
			frappe.throw(
				f"Journey Plan cannot overlap with existing record: {range_exists}. Please select a different date range.",
				title="Journey Plan Overlap Error",
				exc=frappe.ValidationError
			)

	def after_insert(self):
		comment_doc = frappe.get_doc({
			"doctype": "Comment",
			"reference_doctype": "Journey Plan",
			"reference_name": self.name,
			"comment_type": "Workflow",
			"content": self.workflow_state
		})
		comment_doc.insert(ignore_permissions=True)