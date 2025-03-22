import frappe
from frappe.utils import now_datetime

def close_expired_rfqs():
    """Automatically closes RFQs where the quotation submission deadline has passed."""
    rfqs = frappe.get_all(
        "Request for Quotation", 
        filters={"docstatus": 1},  # Ensure we're processing only submitted RFQs
        fields=["name", "custom_quotation_submission_deadline"]
    )

    closed_rfqs = []  # To log RFQs that were closed

    for rfq in rfqs:
        if rfq.custom_quotation_submission_deadline and now_datetime() > rfq.custom_quotation_submission_deadline:
            # Update both status and docstatus
            frappe.db.set_value("Request for Quotation", rfq.name, {
                "status": "Closed",
                "docstatus": 2  # Setting docstatus to 2 (Cancelled)
            })
            closed_rfqs.append(rfq.name)

    # Commit the changes once after the loop
    frappe.db.commit()
    
    # Log the updates
    if closed_rfqs:
        frappe.logger().info(f"Closed {len(closed_rfqs)} expired RFQs: {', '.join(closed_rfqs)}")
