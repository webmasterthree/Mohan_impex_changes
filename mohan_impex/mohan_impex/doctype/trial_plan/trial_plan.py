# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.form.assign_to import add as add_assignment, remove as remove_assignment


class TrialPlan(Document):
    def before_save(self):
        if self.conduct_by == "Self":
            self.assigned_to_emp = self.created_by_emp
        # create_trial_target(self)
        update_assigned_to(self)
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

    def after_insert(self):
        comment_doc = frappe.get_doc({
            "doctype": "Comment",
            "reference_doctype": "Trial Plan",
            "reference_name": self.name,
            "comment_type": "Workflow",
            "content": self.workflow_state
        })
        comment_doc.insert(ignore_permissions=True)
        create_trial_target(self)

def create_trial_target(trial_plan_doc):
    for item in trial_plan_doc.trial_plan_table:
        if item.item_code and item.segment and item.name and not item.trial_target:
            existing_trial_target = frappe.db.get_value("Trial Target", {"product": item.segment, "item_code": item.item_code, "trial_plan": trial_plan_doc.name, "trial_plan_row": item.name})
            if existing_trial_target:
                frappe.delete_doc("Trial Target", existing_trial_target, ignore_permissions=True, force=True)
            trial_target = frappe.new_doc("Trial Target")
            trial_target.update({
                "segment": item.segment,
                "item_code": item.item_code,
                "trial_plan": trial_plan_doc.name,
                "trial_plan_row": item.name
            })
            trial_target.flags.ignore_links = True
            trial_target.save()

            item.db_set("trial_target", trial_target.name)

            trial_target_template = frappe.get_all("Trial Template Table", {"parent": item.item_code}, ["trial_parameter", "type", "idx"])
            if trial_target_template:
                for idx, trial_target_template in enumerate(trial_target_template):
                    trial_target_table = frappe.new_doc("Trial Target Table")
                    trial_target_table.update({
                        "parentfield": "trial_target_table",
                        "parenttype": "Trial Target",
                        "parent": trial_target.name,
                        "trial_parameter": trial_target_template.trial_parameter,
                        "type": trial_target_template.type
                    })
                    trial_target_table.save()
    trial_target_rows = frappe.get_all("Trial Target", filters={"trial_plan": trial_plan_doc.name}, pluck="trial_plan_row")
    trial_target_names = [item.name for item in trial_plan_doc.trial_plan_table if item.name]
    
    delete_trial_targets = [name for name in trial_target_rows if name not in trial_target_names]
    frappe.db.delete("Trial Target", {"trial_plan": trial_plan_doc.name, "trial_plan_row": ("IN", delete_trial_targets)})

def update_assigned_to(self):
    previous_value = self.get_doc_before_save().assigned_to_emp if self.get_doc_before_save() else None
    if previous_value != self.assigned_to_emp:
        if previous_value:
            user_id = frappe.get_value("Employee", {"name": previous_value}, "user_id")
            frappe.db.set_value("ToDo", {"reference_type": self.doctype, "reference_name": self.name, "allocated_to": user_id, "status": "Open"}, "status", "Cancelled")
        if self.conduct_by == "TSM Required" and self.assigned_to_emp:
            user_id = frappe.get_value("Employee", {"name": self.assigned_to_emp}, "user_id")
            add_assignment({"doctype": self.doctype, "name": self.name, "assign_to": [user_id]})
        trial_target_list = frappe.get_all("Trial Target", {"trial_plan": self.name}, ["name", "assigned_to_emp"])
        for trial_target in trial_target_list:
            frappe.db.set_value("Trial Target", trial_target["name"], "assigned_to_emp", self.assigned_to_emp)