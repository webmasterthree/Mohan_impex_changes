import frappe

@frappe.whitelist()
def check_in():
    res = frappe.db.get_all(
        "Employee Checkin",
        fields=["employee","time","latitude","longitude"]
    )
    return res

