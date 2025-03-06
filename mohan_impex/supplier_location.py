import frappe
@frappe.whitelist()
def location(doctype, txt, searchfield, start, page_len, filters):
    custom_company = filters.get("custom_company") if filters else None

    if not custom_company:
        return []

    return frappe.db.sql("""
        SELECT 
            supplier.name, 
            CONCAT(supplier.name, ' - ', COALESCE(supplier.custom_location, 'Not Specified'))
        FROM `tabSupplier` supplier
        WHERE supplier.custom_company = %s
        AND supplier.docstatus < 2
        AND (supplier.name LIKE %s OR supplier.custom_location LIKE %s)
        ORDER BY supplier.name ASC
        LIMIT %s, %s
    """, (custom_company, f"%{txt}%", f"%{txt}%", start, page_len))


