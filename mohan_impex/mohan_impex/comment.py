import frappe
from bs4 import BeautifulSoup
from frappe.model.workflow import apply_workflow
from mohan_impex.api import get_exception

def status_update(self, method):
    doctype = self.reference_doctype
    ref_doctypes = ["Trial Plan", "Customer Visit Management", "Sample Requisition", "Journey Plan", "Sales Order", "Issue", "Marketing Collateral Request", "Customer"]
    if doctype in ref_doctypes and self.comment_type in ["Comment", "Workflow"]:
        ref_name = self.reference_name
        ref_doc = frappe.get_doc(doctype, ref_name)
        status = ref_doc.get("workflow_state")
        frappe.db.set_value("Comment", self.name, {
            'workflow_state': status,
            "comment_by": frappe.session.user
        })

@frappe.whitelist()
def get_comments(doctype, docname):
    comments = frappe.get_all("Comment", {"reference_doctype": doctype, "reference_name": docname, "comment_type": ["in", ["Comment", "Workflow"]]}, ["content", "comment_type", "owner", "creation", "workflow_state"], order_by="creation")
    for comment in comments:
        comment["comments"] = BeautifulSoup(comment["content"], "html.parser").get_text(separator=" ").strip()
        comment["status"] = comment["workflow_state"]
        comment["name"], comment["role"] = frappe.get_value("User", {"name": comment["owner"]}, ["full_name as name", "role_profile_name as role"])
        if comment["name"] == "Administrator":
            comment["role"] = "Administrator"
        comment["date"] = comment["creation"].date()
        comment["time"] = comment["creation"].strftime("%H:%M:%S")
        comment.pop("content")
        comment.pop("owner")
        comment.pop("creation")
        comment.pop("workflow_state")
    return comments

@frappe.whitelist()
def create_comment():
    doctype = frappe.form_dict.get("doctype")
    docname = frappe.form_dict.get("docname")
    comment = frappe.form_dict.get("comment")
    status = frappe.form_dict.get("status")
    try:
        if status:
            workflow_status_update(doctype, docname, status)
            if frappe.local.response.get('http_status_code') == 404:
                return
        comment_doc = frappe.get_doc({
            "doctype": "Comment",
            "reference_doctype": doctype,
            "reference_name": docname,
            "comment_type": "Comment",
            "content": comment
        })
        comment_doc.insert(ignore_permissions=True)
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Successfully made the comment"
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def workflow_status_update(doctype, docname, status):
    try:
        doc = frappe.get_doc(doctype, docname)
        apply_workflow(doc, status)
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Status has been changed to {status}"
        return 
    except Exception as err:
        get_exception(err)

def update_comment_by(self, method):
    if not self.comment_by:
        self.comment_by = frappe.get_value("User", {"name": frappe.session.user}, "full_name") or frappe.session.user
