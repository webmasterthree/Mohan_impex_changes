# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TrialTarget(Document):
	@frappe.whitelist()
	def validate_trial(self):
		if not self.batch_no:
			return "Batch No is required"
		if not self.no_of_batches:
			return "No of Batches is required"
		if not self.mfg_date:
			return "Manufacturing Date is required"
		if not self.batch_size:
			return "Batch Size is required"
		if not self.batch_uom:
			return "Batch UOM is required"
		if self.has_competitor:
			if not self.competitor_brand:
				return "Competitor Brand is required"
			if not self.comp_item:
				return "Competitor Item is required"
			if not self.reason_for_competition:
				return "Reason for Competition is required"
			if self.reason_for_competition == "Others":
				if not self.competition_remarks:
					return "Competition Remarks is required"
			if self.competitor_brand == "Other" and not self.comp_brand_remarks:
				return "Competitor Brand Remarks is required"
			if self.comp_item == "Other" and not self.comp_item_remarks:
				return "Competitor Item Remarks is required"
			if not self.current_dosage:
				return "Current Dosage is required"
			if not self.dosage_uom:
				return "Dosage UOM is required"
		if self.demo_result == "Unsuccessful":
			if not self.reason:
				return "Reason is required"
			if self.reason == "Others":
				if not self.reason_remarks:
					return "Reason Remarks is required"
		if not self.is_order_recieved:
			if not self.ord_nrc_reason:
				return "Order Not Recieved Reason is required"
			if self.ord_nrc_reason == "Stock available at customer point" and not self.next_expec_order_date:
				return "Next Expected Order Date is required"
			if self.ord_nrc_reason == "Others":
				if not self.ord_nrc_remarks:
					return "Order Not Recieved Remarks is required"
		if self.is_order_recieved:
			if not self.month_cons:
				return "Monthly Consumption is required"
			if not self.month_cons_uom:
				return "Monthly Consumption UOM is required"
		for trial_row in self.trial_target_table:
			if trial_row.type == "Satisfaction Status":
				if not trial_row.satisfaction_status:
					return f"Satisfaction Status is required for {trial_row.trial_parameter}"
			if trial_row.type == "Minutes":
				if not trial_row.minutes:
					return f"Minutes is required for {trial_row.trial_parameter}"
			if trial_row.type == "Temperature":
				if not trial_row.temperature:
					return f"Temperature is required for {trial_row.trial_parameter}"
		# if not self.trial_target_table:
		# 	return "Trial Plan is required"
	
	@frappe.whitelist()
	def update_trial_status(self):
		frappe.set_value("Trial Plan Table", self.trial_plan_row, "trial_status", "Completed")
		cvm_trial_id = frappe.get_value("Trial Plan Table", self.trial_plan_row, "cvm_trial_id")
		if cvm_trial_id: frappe.set_value("CVM Trial Table", cvm_trial_id, "report", "Completed")

@frappe.whitelist()
def get_item_trial_template(item_code):
	item_trial_temp = frappe.get_all("Trial Template Table", {"parent": item_code}, ["trial_parameter", "type"])
	return item_trial_temp