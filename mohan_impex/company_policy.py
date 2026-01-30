import frappe

@frappe.whitelist()
def company_policy():
    policy = frappe.db.get_all(
        "Company Policy",
        fields=["name", "policy_title", "policy_document"],
        filters={"status": "Active"}
    )
    return policy
