import frappe
import math
from mohan_impex.api import get_exception
from mohan_impex.api.auth import has_cp


@frappe.whitelist()
def default_warehouse():
    settings = frappe.get_single("Mohan Impex Settings")
    return settings.default_warehouse


@frappe.whitelist()
def price_list():
    try:
        limit = frappe.form_dict.get("limit")
        current_page = frappe.form_dict.get("current_page")

        if not limit or not current_page:
            frappe.local.response["http_status_code"] = 400
            frappe.local.response["status"] = False
            frappe.local.response["message"] = "Either limit or current page is missing"
            return

        limit = int(limit)
        current_page = int(current_page)
        offset = limit * (current_page - 1)

        # customer_type default
        if not has_cp() or not frappe.form_dict.get("customer_type"):
            customer_type = "DP"
        else:
            customer_type = frappe.form_dict.get("customer_type")

        # warehouse default (if not passed)
        warehouse = frappe.form_dict.get("warehouse")
        if not warehouse:
            warehouse = default_warehouse()  

        condition = ""

        if frappe.form_dict.get("search_text"):
            txt = frappe.db.escape(f"%{frappe.form_dict.get('search_text')}%")
            condition += f" AND (item_code LIKE {txt} OR item_name LIKE {txt})"

        if frappe.form_dict.get("item_category"):
            condition += f" AND item_category = {frappe.db.escape(frappe.form_dict.get('item_category'))}"

        if warehouse:
            condition += f" AND warehouse = {frappe.db.escape(warehouse)}"

        if customer_type:
            condition += f" AND customer_type = {frappe.db.escape(customer_type)}"

        price_info_query = f"""
            WITH RankedPrices AS (
                SELECT
                    ip.item_code,
                    ip.item_name,
                    ip.item_category,
                    ip.warehouse,
                    w.warehouse_name,
                    ip.price_list_rate,
                    ip.customer_type,
                    ROW_NUMBER() OVER (
                        PARTITION BY ip.item_code
                        ORDER BY ip.modified DESC
                    ) AS rn
                FROM `tabItem Price` ip
                LEFT JOIN `tabWarehouse` w
                    ON w.name = ip.warehouse
            )
            SELECT
                item_code,
                item_name,
                item_category,
                customer_type,
                price_list_rate,
                warehouse,
                warehouse_name,
                COUNT(*) OVER() AS total_count
            FROM RankedPrices
            WHERE rn = 1 {condition}
            LIMIT %s OFFSET %s
        """

        price_info = frappe.db.sql(price_info_query, (limit, offset), as_dict=True)

        total_count = price_info[0]["total_count"] if price_info else 0
        page_count = math.ceil(total_count / limit) if limit else 0

        frappe.local.response["http_status_code"] = 200
        frappe.local.response["status"] = True
        frappe.local.response["message"] = "Price list has been successfully fetched"
        frappe.local.response["data"] = [{
            "records": price_info,
            "total_count": total_count,
            "page_count": page_count,
            "current_page": current_page,
            "warehouse": warehouse,   # helpful for debugging
            "customer_type_used": customer_type
        }]

    except Exception as err:
        get_exception(err)
