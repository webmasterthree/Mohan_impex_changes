import frappe


@frappe.whitelist()
def competitor_list():
    try:
        competitors = frappe.get_list("Competitor", fields=["name"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Competitors fetched successfully"
        frappe.local.response['data'] = competitors
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"Error fetching competitors: {err}"

@frappe.whitelist()
def batch_list():
    try:
        item_code = frappe.form_dict.get("item_code")
        if not item_code:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Item code must be provided"
            return
        batches = frappe.get_list("Batch", filters={"item": item_code, "disabled": 0}, fields=["name", "manufacturing_date", "stock_uom"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Batches fetched successfully"
        frappe.local.response['data'] = batches
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"Error fetching batches: {err}"