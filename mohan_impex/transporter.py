import frappe
from collections import defaultdict

@frappe.whitelist()
def get_supplier_driver_map():
    """Returns a mapping of transporter → list of driver dicts (with name and full_name)."""
    drivers = frappe.db.get_all('Driver', fields=["name", "full_name", "transporter"])

    supplier_driver_map = defaultdict(list)
    for driver in drivers:
        if driver['transporter']:
            supplier_driver_map[driver['transporter']].append({
                "name": driver["name"],
                "full_name": driver["full_name"]
            })

    return dict(supplier_driver_map)



import frappe

@frappe.whitelist()
def rfq_status(name):
    transporter_count = frappe.db.count(
        "Transporters",
        filters={
            "parent": name,
            "parenttype": "Transport RFQ",
            "parentfield": "transporters",
            "docstatus": 1
        }
    )

    return {
        "name": name,
        "transporter_count": transporter_count
    }



@frappe.whitelist()
def received_quotation_count(transport):
    return {
        "transport": transport,
        "quotation_count": frappe.db.count(
            "RFQ Quotation",
            filters={
                "docstatus": 1,
                "transport": transport
            }
        )
    }



@frappe.whitelist()
def quotation_receive_status(rfq_name):
    transporter_count = frappe.db.count(
        "Transporters",
        filters={
            "parent": rfq_name,
            "parenttype": "Transport RFQ",
            "parentfield": "transporters",
            "docstatus": 1
        }
    )

    quotation_count = frappe.db.count(
        "RFQ Quotation",
        filters={
            "docstatus": ["!=", 2],   # exclude cancelled
            "transport": rfq_name
        }
    )

    status = "Fully Received" if transporter_count == quotation_count else "Partially Received"

    return {
        "rfq_name": rfq_name,
        "transporter_count": transporter_count,
        "quotation_count": quotation_count,
        "status": status
    }





@frappe.whitelist()
def mark_rejected(transport=None):
	if not transport:
		return []

	rows = frappe.db.get_all(
		"RFQ Quotation",
		filters={"transport": transport,"docstatus":"1"},
		fields=["name"],
		order_by="creation desc"
	)

	return [r["name"] for r in rows]
