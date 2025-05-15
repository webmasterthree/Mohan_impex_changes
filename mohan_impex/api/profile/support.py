import frappe

@frappe.whitelist()
def get_support_and_questions():
    try:
        contact_support_list = frappe.get_all("Contact Support", ["support_type", "support_content"])
        freq_asked_questions = frappe.get_all("Frequently Asked Questions", {"status": "Published"}, ["question", "answer"])
        data = {
            "contact_support": contact_support_list,
            "freq_asked_questions": freq_asked_questions
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Support and Frequently Asked Questions list has been successfully fetched"
        frappe.local.response['data'] = data
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"