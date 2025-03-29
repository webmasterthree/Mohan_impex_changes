import frappe

def updated_workflow_state(self, status):
    comment_doc = frappe.get_doc({
        "doctype": "Comment",
        "reference_doctype": "Issue",
        "reference_name": self.name,
        "comment_type": "Workflow",
        "content": self.workflow_state
    })
    comment_doc.insert(ignore_permissions=True)