# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import re

class State(Document):

	def before_insert(self):
		self.autoname()

	def autoname(self):
		if frappe.get_system_settings().get("country") == "India":
			self.name = self.state
		else:
			country_code = country = frappe.db.get_value("Country", self.country, "code").upper() or self.country[:2].upper()
			state_slug = make_slug(self.state)
			self.name = f"{country_code}-{state_slug}"

def make_slug(text):
	return re.sub(r'[^A-Z0-9]+', '', text.upper())