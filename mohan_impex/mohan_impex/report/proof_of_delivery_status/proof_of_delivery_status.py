# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": "Customer", "fieldname": "customer", "fieldtype": "Data", "width": 200},
		{"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 120},
		{"label": "Proof of Delivery Status", "fieldname": "proof_of_delivery_status", "fieldtype": "Data", "width": 180},
	]

def get_data(filters):
	conditions = {}
	if filters.get("proof_of_delivery_status"):
		conditions["custom_proof_of_delivery_status"] = filters["proof_of_delivery_status"]

	return frappe.db.get_all(
		"Sales Invoice",
		fields=["customer", "grand_total", "custom_proof_of_delivery_status as proof_of_delivery_status"],
		filters={**conditions, "docstatus": 1},
		order_by="posting_date desc"
	)
