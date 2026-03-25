import frappe

@frappe.whitelist()
def active_shift(employee):
    res = frappe.db.get_all(
        "Shift Assignment",
        filters={
            "status": "Active",
            "employee": employee
        },
        fields=["name", "employee"]
    )
    return res