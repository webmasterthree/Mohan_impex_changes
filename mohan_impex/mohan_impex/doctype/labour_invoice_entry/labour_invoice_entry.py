# Copyright (c) 2026, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, today


class LabourInvoiceEntry(Document):
	def on_submit(self):
		create_purchase_invoice(self)


def create_purchase_invoice(doc):
    if not doc.supplier:
        frappe.throw("Supplier is required")

    pi = frappe.new_doc("Purchase Invoice")
    pi.supplier = doc.supplier
    pi.company = doc.company
    pi.branches = "Kolkata"
    pi.posting_date = doc.posting_date
    pi.set_posting_time = 1
    pi.bill_date = today()
    pi.bill_no = doc.name

    for row in doc.labour_details:
        if row.total and row.total > 0:
            pi.append("items", {
                "item_code": get_item_by_gender(row.gender),
                "qty": 1,
                "rate": row.total,
		"branches":"Kolkata",
		"expense_account":"Forwarding Charge - MISL"
            })

    pi.insert()
    pi.submit()

    frappe.msgprint(f"Purchase Invoice {pi.name} Created")


def get_item_by_gender(gender):
    if gender == "Male":
        return "Male Labour"
    elif gender == "Female":
        return "Female Labour"
