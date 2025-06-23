import frappe
from mohan_impex.api import get_exception

@frappe.whitelist()
def get_legal_info():
    try:
        legal_info = frappe.get_all("Legal Information", {"status": "Published"}, ["legal_document_name", "legal_content"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Legal Information list has been successfully fetched"
        frappe.local.response['data'] = legal_info
    except Exception as err:
        get_exception(err)