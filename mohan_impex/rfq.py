import frappe
from frappe import _

def send_rfq_email(doc, method):
    """
    Send RFQ email to suppliers listed in the 'suppliers' child table of the RFQ.
    """
    if not doc.suppliers:
        return

    supplier_emails = set()  # Store unique emails

    # Loop through the suppliers in the RFQ
    for supplier in doc.suppliers:
        if supplier.send_email and supplier.email_id:  # Check if email should be sent
            supplier_emails.add(supplier.email_id)

    if not supplier_emails:
        frappe.msgprint(_("No suppliers with email addresses found in this RFQ."))
        return

    # Load the RFQ Email Template
    email_template = frappe.get_doc("Email Template", "Request For Quotation")
    
    # Render the template with actual RFQ details
    message = frappe.render_template(email_template.response, {"doc": doc})
    
    # Send the email using Frappe's email system
    frappe.sendmail(
        recipients=list(supplier_emails),
        subject=email_template.subject.format(doc=doc),
        message=message,
        reference_doctype=doc.doctype,
        reference_name=doc.name
    )

    frappe.msgprint(_("RFQ emails sent successfully to suppliers in this RFQ!"))
