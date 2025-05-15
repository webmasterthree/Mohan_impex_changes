import frappe

@frappe.whitelist()
def get_legal_info():
    try:
        legal_info = frappe.get_all("Legal Information", {"status": "Published"}, ["legal_document_name", "legal_content"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Legal Information list has been successfully fetched"
        frappe.local.response['data'] = legal_info
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"