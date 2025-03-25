import frappe


def update_customer_edit_needed(self, method):
    if self.cust_edit_needed:
        frappe.db.set_value("Customer", self.customer, "cust_edit_needed", self.cust_edit_needed)

