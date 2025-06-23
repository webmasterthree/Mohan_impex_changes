import frappe
import math
from mohan_impex.api import get_exception

@frappe.whitelist()
def scheme_list():
    try:
        limit = frappe.form_dict.get("limit")
        current_page = frappe.form_dict.get("current_page")
        if not limit or not current_page:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Either limit or current page is missing"
            return
        current_page = int(current_page)
        limit = int(limit)
        offset = limit * (current_page - 1)
        pagination = "limit %s offset %s"%(limit, offset)
        # scheme_list = frappe.get_list("Pricing Rule", scheme_filter, scheme_fields, limit_start=offset, limit_page_length=limit)
        order_by = " order by creation desc "
        query = """
            select title, scheme_type, description, discount_percentage, terms_and_conditions, valid_upto, min_qty, COUNT(*) OVER() AS total_count
            from `tabPricing Rule`
            where rate_or_discount = "Discount Percentage" and selling = 1 and disable = 0
        """
        filter_checks = {
            "scheme_type": "scheme_type",
        }
        if frappe.form_dict.get("search_text"):
            or_filters = """ and (name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_by
        query += pagination
        scheme_list = frappe.db.sql(query, as_dict=True)
        total_count = 0
        if scheme_list:
            total_count = scheme_list[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": scheme_list,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Scheme list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)
