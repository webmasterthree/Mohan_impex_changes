import frappe


@frappe.whitelist()
def competitor_list():
    frappe.local.response['data'] = frappe.get_list("Competitor", fields=["name"])