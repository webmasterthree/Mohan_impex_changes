# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MarketingCollateralRequest(Document):
	def after_insert(self):
		comment_doc = frappe.get_doc({
			"doctype": "Comment",
			"reference_doctype": "Marketing Collateral Request",
			"reference_name": self.name,
			"comment_type": "Workflow",
			"content": self.workflow_state
		})
		comment_doc.insert(ignore_permissions=True)
