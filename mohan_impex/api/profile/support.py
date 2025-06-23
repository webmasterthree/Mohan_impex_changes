import frappe
from mohan_impex.api import get_signed_token, get_exception

@frappe.whitelist()
def get_support_and_questions():
    try:
        contact_support_list = frappe.get_all("Contact Support", ["support_type", "support_content", "support_image"])
        for contact in contact_support_list:
            contact["support_image"] = get_signed_token(contact["support_image"])
        freq_asked_questions = frappe.get_all("Frequently Asked Questions", {"status": "Published"}, ["question", "answer"])
        data = {
            "contact_support": contact_support_list,
            "freq_asked_questions": freq_asked_questions
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Support and Frequently Asked Questions list has been successfully fetched"
        frappe.local.response['data'] = data
    except Exception as err:
        get_exception(err)