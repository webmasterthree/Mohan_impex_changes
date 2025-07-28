import frappe
from frappe import whitelist

@whitelist(allow_guest=True)
def get_employees():
    return frappe.db.get_all(
        "Employee",
        fields=["name", "employee_name", "image", "company", "date_of_birth", "gender"]
    )


import frappe

@frappe.whitelist(allow_guest=True)
def create_public_todo(description):
    if not description:
        frappe.throw("Description is required.")

    # Insert without permission checks (since guest has no perms)
    doc = frappe.get_doc({
        "doctype": "ToDo",
        "description": description,
        "assigned_by": "Guest"
    })
    doc.insert(ignore_permissions=True)
    return {"name": doc.name}

SUPPORTED_FIELD_TYPES = [
	"Link",
	"Select",
	"Small Text",
	"Text",
	"Long Text",
	"Text Editor",
	"Table",
	"Check",
	"Data",
	"Float",
	"Int",
	"Section Break",
	"Date",
	"Time",
	"Datetime",
	"Currency",
	"Attach",
]

@frappe.whitelist(allow_guest=True)
def get_doctype_fields(doctype: str) -> list[dict]:
    try:
        meta = frappe.get_meta(doctype)
    except frappe.DoesNotExistError:
        frappe.throw(f"Doctype {doctype} does not exist.")

    return [
        field
        for field in meta.fields
        if field.fieldtype in SUPPORTED_FIELD_TYPES and field.fieldname != "amended_from"
    ]



@frappe.whitelist()
def get_my_assignment_notifications():
    return frappe.get_all(
        "Notification Log",
        filters={
            "type": "Assignment",
            "for_user": frappe.session.user
        },
        fields=[
            "creation", "document_name", "document_type",
            "email_content", "for_user", "from_user", "subject"
        ],
        order_by="creation desc",
        limit_page_length=20
    )



import frappe
from frappe import _
from frappe.utils.print_format import download_pdf

@frappe.whitelist()
def download_salary_slip(name: str):
    """
    Generates and returns the Salary Slip PDF file as a base64-encoded blob
    or streams the PDF directly for download.
    """
    if not name:
        frappe.throw(_("Salary Slip name is required."))

    # Make sure the user has access to the document
    salary_slip = frappe.get_doc("Salary Slip", name)
    if not salary_slip.has_permission("read"):
        frappe.throw(_("You are not authorized to view this Salary Slip."))

    # Check if it's submitted
    if salary_slip.docstatus != 1:
        frappe.throw(_("Only submitted Salary Slips can be downloaded."))

    # Use default or custom print format
    default_print_format = frappe.get_meta("Salary Slip").default_print_format or "Standard"

    try:
        # This sets frappe.local.response with the file data
        download_pdf("Salary Slip", name, format=default_print_format)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Download Salary Slip Error")
        frappe.throw(_("Failed to generate Salary Slip PDF."))

    # Return file content as base64 if needed (frontend usually expects a blob)
    return {
        "filename": f"{name}.pdf",
        "content_type": frappe.local.response.type,
        "base64": frappe.safe_encode(frappe.local.response.filecontent, "base64"),
    }






import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_notifications(to_user):
    return frappe.db.get_all(
        "PWA Notification",
        filters={"to_user": to_user},
        fields=[
            "to_user", "from_user", "message",
            "reference_document_type", "reference_document_name", "read"
        ]
    )
