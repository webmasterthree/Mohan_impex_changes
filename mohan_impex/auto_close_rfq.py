import frappe
from frappe.utils import now_datetime

def close_expired_rfqs():
    """Automatically marks RFQs as closed in custom_rfq_actual_status where the quotation submission deadline has passed."""
    rfqs = frappe.get_all(
        "Request for Quotation", 
        filters={"docstatus": 1},  # Only submitted RFQs
        fields=["name", "custom_quotation_submission_deadline", "custom_rfq_actual_status"]
    )

    closed_rfqs = []

    for rfq in rfqs:
        if (
            rfq.custom_quotation_submission_deadline 
            and now_datetime() > rfq.custom_quotation_submission_deadline
            and rfq.custom_rfq_actual_status != "Closed"
        ):
            frappe.db.set_value("Request for Quotation", rfq.name, "custom_rfq_actual_status", "Closed")
            closed_rfqs.append(rfq.name)

    frappe.db.commit()

    if closed_rfqs:
        frappe.logger().info(f"Marked {len(closed_rfqs)} RFQs as Closed (custom_rfq_actual_status): {', '.join(closed_rfqs)}")

