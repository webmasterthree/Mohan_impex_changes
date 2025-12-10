import frappe

@frappe.whitelist()
def get_address():
    result = frappe.db.get_all(
        "Address",
        fields=[
            "address_line1",
            "address_line2",
            "district",
            "city",
            "state",
            "county",
            "pincode",
            "email_id",
            "phone",
            "gstin",
        ],
        filters={"name": "Kolkata HQ-Billing"},
        limit=1,
    )
    return result[0] if result else {}
