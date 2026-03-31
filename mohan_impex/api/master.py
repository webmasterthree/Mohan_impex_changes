import frappe

@frappe.whitelist()
def get_products():
    query = """
        select product_name
        from `tabProduct`
    """
    if frappe.form_dict.get("search_text"):
        query += """where (product_name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
    item_templates = frappe.db.sql(query, as_dict=True)
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Products fetched successfully"
    frappe.local.response['data'] = item_templates