import frappe
import math
from datetime import datetime, timedelta
from erpnext.accounts.party import get_dashboard_info
from mohan_impex.api.sales_order import get_role_filter
from mohan_impex.api import get_exception, get_self_filter_status
from mohan_impex.api.auth import has_cp

@frappe.whitelist()
def my_customer_list():
    try:
        form = frappe.form_dict

        conditions = ["disabled = 0", "kyc_status = 'Completed'"]

        if form.get("search_text"):
            conditions.append("""
                (name LIKE %(search)s OR 
                 customer_name LIKE %(search)s)
            """)

        if form.get("customer_level"):
            conditions.append("customer_level = %(customer_level)s")

        if form.get("state"):
            conditions.append("state = %(state)s")

        if form.get("district"):
            conditions.append("district = %(district)s")

        if form.get("city"):
            conditions.append("city = %(city)s")

        condition_sql = " AND ".join(conditions)

        query = f"""
            SELECT 
                name,
                customer_name,
                city,
                district,
                state,
                customer_level
            FROM `tabCustomer`
            WHERE {condition_sql}
            ORDER BY creation DESC
        """

        params = {
            "search": f"%{form.get('search_text')}%" if form.get("search_text") else None,
            "customer_level": form.get("customer_level"),
            "state": form.get("state"),
            "district": form.get("district"),
            "city": form.get("city")
        }

        data = frappe.db.sql(query, params, as_dict=True)

        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Customer list fetched"
        frappe.local.response['data'] = data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "my_customer_list error")
        frappe.local.response['status'] = False
        frappe.local.response['message'] = str(e)