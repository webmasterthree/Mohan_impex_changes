import frappe
import re

@frappe.whitelist()
def get_remarks(reference_name):
    if not reference_name:
        return ""

    content = frappe.db.get_value(
        "Comment",
        filters={
            "reference_doctype": "Sales Order",
            "reference_name": reference_name,
            "comment_type": "Comment",
        },
        fieldname="content",
        order_by="creation desc",
    )

    if not content:
        return ""

    # Extract the text after "Remarks:</span>"
    m = re.search(r"Remarks:\s*</span>\s*([^<]+)", content, flags=re.IGNORECASE)
    return (m.group(1).strip() if m else "")
