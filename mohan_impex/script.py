import frappe
import pprint

def find():
    doctype = "Transport RFQ"
    query = f"""
        SELECT 
            df.parent AS doctype,
            df.fieldname,
            df.label,
            df.fieldtype,
            df.options
        FROM (
            SELECT 
                parent, fieldname, label, fieldtype, options
            FROM `tabDocField`
            WHERE parent = '{doctype}'
            AND fieldtype IN ('Link', 'Table', 'Table MultiSelect')

            UNION ALL

            SELECT 
                dt AS parent, fieldname, label, fieldtype, options
            FROM `tabCustom Field`
            WHERE dt = '{doctype}'
            AND fieldtype IN ('Link', 'Table', 'Table MultiSelect')
        ) AS df

        UNION ALL

        SELECT 
            CONCAT('{doctype} → ', child.options) AS doctype_path,
            c.fieldname,
            c.label,
            c.fieldtype,
            c.options
        FROM (
            SELECT options
            FROM `tabDocField`
            WHERE parent = '{doctype}'
            AND fieldtype IN ('Table', 'Table MultiSelect')

            UNION

            SELECT options
            FROM `tabCustom Field`
            WHERE dt = '{doctype}'
            AND fieldtype IN ('Table', 'Table MultiSelect')
        ) AS child
        JOIN (
            SELECT 
                parent, fieldname, label, fieldtype, options
            FROM `tabDocField`
            WHERE fieldtype IN ('Link', 'Table', 'Table MultiSelect')

            UNION ALL

            SELECT 
                dt AS parent, fieldname, label, fieldtype, options
            FROM `tabCustom Field`
            WHERE fieldtype IN ('Link', 'Table', 'Table MultiSelect')
        ) AS c 
            ON c.parent = child.options

        ORDER BY doctype, fieldtype, fieldname;


    """
    result = frappe.db.sql(query, as_dict=1)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)