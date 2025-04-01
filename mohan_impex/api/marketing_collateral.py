import frappe
import math
from mohan_impex.api import get_signed_token

@frappe.whitelist()
def digital_mc_list():
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
        order_by = " order by creation desc "
        query = """
            select name, marketing_collateral_name, collateral_attachment, thumbnail_image, COUNT(*) OVER() AS total_count
            from `tabDigital Marketing Collateral`
            WHERE status = "Published"
        """
        if frappe.form_dict.get("search_text"):
            or_filters = """ and (marketing_collateral_name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        query += order_by
        query += pagination
        dmc_info = frappe.db.sql(query, as_dict=True)
        for dmc in dmc_info:
            dmc["filename"], dmc["file_type"] = frappe.get_value("File", {"file_url": dmc['collateral_attachment']}, ["file_name", "file_type"])
            dmc["collateral_attachment"] = get_signed_token(dmc['collateral_attachment'])
            dmc["thumbnail_image"] = get_signed_token(dmc['thumbnail_image'])
        total_count = 0
        if dmc_info:
            total_count = dmc_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": dmc_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Digital Marketing Collateral list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"