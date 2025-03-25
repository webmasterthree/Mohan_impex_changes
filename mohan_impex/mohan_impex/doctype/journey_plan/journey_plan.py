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
