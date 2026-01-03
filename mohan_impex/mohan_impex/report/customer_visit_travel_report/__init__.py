import frappe

@frappe.whitelist()
def check_in():
    res = frappe.db.get_all(
        fields=["employee","time"]
    )
    return res