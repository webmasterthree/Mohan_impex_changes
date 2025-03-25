# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TrialPlan(Document):
    def before_save(self):
        if self.cust_edit_needed:
            if self.verific_type == "Verified":
                frappe.db.set_value("Customer", self.customer, "cust_edit_needed", self.cust_edit_needed)
            else:
                frappe.db.set_value("Unverified Customer", self.unv_customer, "cust_edit_needed", self.cust_edit_needed)


    @frappe.whitelist()
    def get_contact_and_address(self):
        if self.verific_type == "Verified":
            customer_info = frappe.get_value("Customer", {"name": self.customer}, ["customer_primary_address as address", "customer_primary_contact as contact", "custom_shop as shop", "custom_channel_partner as channel_partner"], as_dict=1)
            customer_info["contact"] = [{"contact": customer_info["contact"]}] if customer_info["contact"] else []
            return customer_info
        elif self.verific_type == "Unverified":
            customer_info = frappe.get_value("Unverified Customer", {"name": self.unv_customer}, ["address", "shop", "channel_partner"], as_dict=1)
            customer_info["contact"] = frappe.get_all("Contact List", {"parent": self.unv_customer}, ["contact"])
            return customer_info

    @frappe.whitelist()
    def get_kyc_status(self):
        kyc_status = frappe.get_value("Customer", self.customer, "kyc_status")
        if kyc_status == "Completed": return True
        else: return False

    # def before_save(self):
        # trial_item_list = []
        # for item in self.product_trial:
        #     if item.trial_template:
        #         trial_name_list = frappe.get_all("Trial Template Table", {"parent": item.trial_template}, ["trial_name"], pluck="trial_name", order_by="idx")
        #         for trial_name in trial_name_list:
        #             trial_item = next(filter(lambda x: x.item_code == item.item_code and x.trial_name == trial_name, self.trial_item_table), None)
        #             if not trial_item:
        #                 dt_item = frappe.new_doc("Trial Item Table")
        #                 dt_item.update({
        #                     "parentfield": "trial_item_table", 
        #                     "parenttype": "Trial Plan",
        #                     "parent": self.name,
        #                     "trial_row_id": item.idx,
        #                     "item_code": item.item_code,
        #                     "trial_name": trial_name
        #                 })
        #                 trial_item_list.append(dt_item)
        #             else:
        #                 trial_item_list.append(trial_item)
        # self.trial_item_table = trial_item_list
