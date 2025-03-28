# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import datetime
import frappe

class JourneyPlan(Document):
	def before_save(self):
		# frappe.errprint(self.workflow_state)
		if (self.workflow_state == "Approved"):
			self.approved_date = datetime.today()

	def after_insert(self):
		comment_doc = frappe.get_doc({
			"doctype": "Comment",
			"reference_doctype": "Journey Plan",
			"reference_name": self.name,
			"comment_type": "Workflow",
			"content": self.workflow_state
		})
		comment_doc.insert(ignore_permissions=True)