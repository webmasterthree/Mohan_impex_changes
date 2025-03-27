import frappe
from frappe.model.workflow import apply_workflow

@frappe.whitelist()
def update_kyc_status(customer, unv_customer=None):
    or_filters = {
        "customer": customer
    }
    if unv_customer:
        frappe.db.set_value("Unverified Customer", unv_customer, {
            "customer": customer,
            "kyc_status": "Completed"
        })
        or_filters.update({"unv_customer": unv_customer})
    cvm_list = frappe.db.get_all("Customer Visit Management", or_filters=or_filters, fields=["name"], pluck="name")
    for cvm in cvm_list:
        frappe.db.set_value("Customer Visit Management", cvm, "kyc_status", "Completed")

def updated_workflow_state(self, status):
    if self.customer_level == "Primary":
        comment_doc = frappe.get_doc({
            "doctype": "Comment",
            "reference_doctype": "Customer",
            "reference_name": self.name,
            "comment_type": "Workflow",
            "content": self.workflow_state
        })
        comment_doc.insert(ignore_permissions=True)
    if self.customer_level == "Secondary" and self.workflow_state == "KYC Pending":
        apply_workflow(self, "Complete KYC")

def validate_dup_unv_id(self, status):
    if self.unv_customer:
        cus_id = frappe.db.exists("Customer", {"unv_customer": self.unv_customer, "name": ["!=", self.name]})
        if cus_id:
            frappe.throw(f"Customer {cus_id} has already been created for the Unverified Customer {self.unv_customer}")
