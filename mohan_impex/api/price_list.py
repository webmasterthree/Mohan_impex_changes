import frappe
import math
from mohan_impex.api import get_exception

@frappe.whitelist()
def price_list():
    try:
        limit = frappe.form_dict.get("limit")
        current_page = frappe.form_dict.get("current_page")
        if not limit or not current_page:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Either limit or current page is missing"
            return
        customer_type = frappe.form_dict.get("customer_type") or "DP"
        current_page = int(current_page)
        limit = int(limit)
        offset = limit * (current_page - 1)
        pagination = "limit %s offset %s"%(limit, offset)
        condition = ""
        if frappe.form_dict.get("search_text"):
            condition = """ and (item_code LIKE "%{0}%" OR item_name LIKE "%{0}%") """.format(frappe.form_dict.get("search_text"))
        if frappe.form_dict.get("item_category"):
            condition = """ and item_category = "{0}" """.format(frappe.form_dict.get("item_category"))
        if customer_type:
            condition = """ and customer_type = "{0}" """.format(customer_type)
        price_info_query = """
            WITH RankedPrices AS (
                SELECT 
                    item_code,
                    item_name,
                    item_category,
                    price_list_rate,
                    customer_type,
                    ROW_NUMBER() OVER (PARTITION BY item_code, customer_type ORDER BY modified asc) AS rn
                FROM `tabItem Price`
                WHERE selling = 1
            )
            SELECT item_code, item_name, item_category, customer_type, price_list_rate, COUNT(*) OVER() AS total_count
            FROM RankedPrices
            WHERE rn = 1 {0}
        """.format(condition)
        price_info_query += pagination
        price_info = frappe.db.sql(price_info_query, as_dict=True)
        total_count = 0
        if price_info:
            total_count = price_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": price_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Price list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)

# price_info_query = f"""
#     WITH RankedData AS (
#         SELECT 
#             ip.item_code AS sku, 
#             ip.item_code AS product_name, 
#             pcp.product_category, 
#             pcp.rate,
#             ROW_NUMBER() OVER (
#                 PARTITION BY ip.item_code, pcp.product_category 
#                 ORDER BY pcp.creation DESC
#             ) AS rn
#         FROM `tabProduct Category Price` AS pcp
#         JOIN `tabItem Price` AS ip ON ip.name = pcp.parent
#     )
#     SELECT sku, product_name, product_category, rate
#     FROM RankedData
#     WHERE rn = 1
#     GROUP BY product_name, product_category;
#         """