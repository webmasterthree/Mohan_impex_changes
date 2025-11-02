# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import re

class District(Document):

	def before_insert(self):
		self.autoname()

	def autoname(self):
    # Fetch linked state and country
		state_info = frappe.db.get_value("State", self.state, ["state", "country"], as_dict=True)
		if not state_info:
			frappe.throw("Please set a valid State before saving the District")

		country_info = frappe.db.get_value("Country", state_info.country, ["code", "name"], as_dict=True)
		if not country_info:
			frappe.throw("Invalid country configuration")

		# Prepare codes
		country_code = make_slug(country_info.code or country_info.name[:3])
		state_code = make_slug(state_info.state)
		district_code = make_slug(self.district)

		# Final Ref ID
		self.name = f"{country_code}-{state_code}-{district_code}"

def make_slug(text):
	return re.sub(r'[^A-Z0-9]', '', text.upper())