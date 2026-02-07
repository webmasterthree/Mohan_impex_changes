# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mohan_impex.api import send_push_notification
from mohan_impex.mohan_impex.comment import create_comment
from mohan_impex.api import create_notification_log

class Announcement(Document):
	def after_insert(self):
		self.send_announcement()

	def send_announcement(self):
		roles = [role.role for role in self.roles]
		users = frappe.get_all("User", filters={"role": ("in", roles)}, pluck="name")
		create_notification_log(
			self, 
			users,
			title=self.subject, 
			body=self.message, 
			doctype=self.doctype, 
			docname=self.name
		)