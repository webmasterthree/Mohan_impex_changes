# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.workflow import apply_workflow, validate_workflow
from frappe.model.document import Document
import frappe
from mohan_impex.item_price import get_item_category_price
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee
from datetime import datetime

class CustomerVisitManagement(Document):
    def before_save(self):
        emp = frappe.get_value('Employee', "user_id", frappe.user, "name")
        self.create_by_emp = emp
        if self.latitude and self.longitude:
            self.map_location = frappe.json.dumps({
                    "type": "FeatureCollection", 
                    "features": [{
                        "type": "Feature", 
                        "properties":{},
                        "geometry": {"type": "Point", "coordinates": [self.latitude, self.longitude]}
                    }]
                })
        kyc_status = ""
        if self.verific_type == "Verified":
            kyc_status = frappe.get_value("Customer", {"name", self.customer}, "kyc_status")
            if self.cust_edit_needed:
                frappe.db.set_value("Customer", self.customer, "cust_edit_needed", self.cust_edit_needed)
        else:
            kyc_status = frappe.get_value("Unverified Customer", {"name", self.unv_customer}, "kyc_status")
            if self.cust_edit_needed:    
                frappe.db.set_value("Unverified Customer", self.unv_customer, "cust_edit_needed", self.cust_edit_needed)
        self.kyc_status = kyc_status

    @frappe.whitelist()
    def get_contact_and_address(self):
        if self.verific_type == "Verified":
            customer_info = frappe.get_value("Customer", {"name": self.customer}, ["customer_primary_address as address", "customer_primary_contact as contact", "custom_shop as shop", "custom_channel_partner as channel_partner"], as_dict=1)
            customer_info["contact"] = frappe.get_all("Contact Phone", {"parent": customer_info.get("contact")}, ["contact_number as contact"]) if customer_info.get("contact") else []
            # customer_info["contact"] = [{"contact": customer_info["contact"]}] if customer_info["contact"] else []
            return customer_info
        elif self.verific_type == "Unverified":
            customer_info = frappe.get_value("Unverified Customer", {"name": self.unv_customer}, ["address", "shop", "channel_partner"], as_dict=1)
            customer_info["contact"] = frappe.get_all("Contact List", {"parent": self.unv_customer}, ["contact"])
            return customer_info

    @frappe.whitelist()
    def get_kyc_status(self):
        is_kyc_done = False
        customer_url = ""
        if self.verific_type == "Verified":
            if self.customer_level == "Primary":
                kyc_status = frappe.get_value("Customer", self.customer, "kyc_status")
                customer_url = frappe.utils.get_url_to_form("Customer", self.customer)
                if kyc_status == "Completed":
                    is_kyc_done = True
            else:
                is_kyc_done = True
        else:
            kyc_status = frappe.get_value("Unverified Customer", self.unv_customer, "kyc_status")
            customer_url = frappe.utils.get_url_to_form("Unverified Customer", self.unv_customer)
            if kyc_status == "Completed":
                is_kyc_done = True
        response = {
            "kyc_status": is_kyc_done,
            "customer_url": customer_url
        }
        return response

    @frappe.whitelist()
    def trial_plan(self):
        trial_plan = frappe.db.exists(
            "Trial Plan", {"cvm": self.name})
        if self.has_trial_plan:
            table_dict = {}
            if self.verific_type == "Verified":
                table_dict.update({"customer": self.customer})
                table_dict.update({"customer_name": self.customer_name})
            else:
                table_dict.update({"unv_customer": self.unv_customer})
                table_dict.update({"unv_customer_name": self.unv_customer_name})
            # if self.trial_type == "Product":
            #     products = [{"product": product.product} for product in self.product_trial]
            #     table_dict.update({"product_trial_table": products})
            # else:
            #     items = [{"item_code": item.item_code} for item in self.item_trial]
            #     table_dict.update({"item_trial_table": items})
            pt_dict = {
                "customer_level":  self.customer_level,
                "channel_partner": self.channel_partner,
                "verific_type": self.verific_type,
                "trial_loc": self.trial_loc,
                "conduct_by": self.conduct_by,
                "shop": self.shop,
                "shop_name": self.shop_name,
                "location": self.location,
                "address_line1": self.address_line1,
                "address_line2": self.address_line2,
                "district": self.district,
                "city": self.district,
                "state": self.state,
                "pincode": self.pincode,
                "visit_start": self.visit_start,
                "visit_end": self.visit_end,
                "visit_duration": self.visit_duration,
                "trial_date": self.trial_date,
                "time": self.time,
                "remarksnotes": self.trial_plan_remarks,
                "created_by_emp": get_session_employee(),
                "area": get_session_employee_area()
            }
            pt_dict.update(table_dict)
            doc = frappe.get_doc("Trial Plan", trial_plan) if trial_plan else frappe.get_doc({
                "doctype": "Trial Plan",
                "cvm": self.name,
                **pt_dict
            })
            trial_row_list = [{"cvm_trial_id": trial_row.name, "product": trial_row.product, "item_code": trial_row.item_code} for trial_row in self.trial_table]
            existing_trial_row = doc.trial_plan_table
            trial_row_to_add_list = []
            trial_row_to_remove_list = []
            for trial_row in trial_row_list:
                if not any(existing_product.product == trial_row["product"] and existing_product.item_code == trial_row["item_code"] for existing_product in existing_trial_row):
                    trial_row_to_add_list.append(trial_row)
            for existing_product in existing_trial_row:
                if not any(trial_row["product"] == existing_product.product and trial_row["item_code"] == existing_product.item_code for trial_row in trial_row_list):
                    trial_row_to_remove_list.append(existing_product.name)
            for trial_row_to_row in trial_row_to_add_list:
                doc.append("trial_plan_table", trial_row_to_row)
            for trial_row_to_remove in trial_row_to_remove_list:
                doc.trial_plan_table = [item for item in doc.trial_plan_table if item.name != trial_row_to_remove]
            for idx, trial_plan in enumerate(doc.trial_plan_table, start=1):
                trial_plan.update({"idx": idx})
            doc.update(pt_dict)
            doc.update({"contact": []})  # Clear existing contacts if updating
            for contact in self.contact:
                doc.append("contact", {"contact": contact.contact})
            doc.save() if trial_plan else doc.insert()
        elif not self.has_trial_plan and trial_plan:
            frappe.delete_doc("Trial Plan", trial_plan)

    @frappe.whitelist()
    def create_order(self, return_so_id=False):
        items = []
        for item in self.product_pitching:
            rate = get_item_category_price(item.item_code, item.item_category)
            items.append({
                "item_code": item.item_code,
                "custom_item_category": item.item_category,
                "competitor": item.competitor,
                "qty": item.qty,
                "rate": rate,
                "price_list_rate": rate
            })
        contact = ""
        if self.contact:
            contact = self.contact[0].contact
        order_dict = {
            "doctype": "Sales Order",
            "customer": self.customer,
            "customer_visit": self.name,
            "customer_level": self.customer_level,
            "contact_person": contact,
            "shipping_address_name": self.location,
            "custom_deal_type": self.deal_type,
            "shop": self.shop,
            "created_by_emp": get_session_employee(),
            "items": items,
            "delivery_date": datetime.today()
        }
        if self.customer_level == "Secondary":
            order_dict.update({
                "custom_channel_partner": self.channel_partner,
                "company": self.channel_partner
            })
        doc = frappe.get_doc(order_dict)
        doc.flags.ignore_mandatory = True
        doc.save()
        if return_so_id:
            response = {
                "so_id": doc.name
            }
            return response
        so_url = frappe.utils.get_url_to_form("Sales Order", doc.name)
        return so_url


@frappe.whitelist()
def get_product_items(product=None):
    item_list = frappe.get_all("Base Components", {"parent": product}, ["item_code"], pluck="item_code")
    return item_list

def test():
    doc = frappe.get_doc("Customer Visit Management", "CVM-2025-01-0025")
    apply_workflow(doc, "Pending")
