# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TrialTarget(Document):
	pass

@frappe.whitelist()
def get_item_trial_template(item_code):
	item_trial_temp = frappe.get_all("Trial Template Table", {"parent": item_code}, ["trial_parameter", "type"])
	return item_trial_temp