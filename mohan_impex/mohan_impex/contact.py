import frappe

def get_contact_numbers(doctype, doc_name):
    query = """
        select cn.name
        from `tabContact Number` as cn
        join `tabDynamic Link` as dl on dl.parent = cn.name
        where dl.link_doctype = "{0}" and dl.link_name = "{1}"
    """.format(doctype, doc_name)
    contact_numbers = frappe.db.sql_list(query)
    return contact_numbers