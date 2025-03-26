import frappe

@frappe.whitelist()
def get_transporters_for_rfq(rfq_name):
    return frappe.db.get_all("Transporters",
        filters={
            "parent": rfq_name,
            "parenttype": "Transport RFQ",
            "select": 1 
        },
        fields=["transporter_name", "quoted_amount", "expected_delivery", "remarks", "select"]
    )
