import frappe
import math
from datetime import datetime, timedelta
from erpnext.accounts.party import get_dashboard_info
from mohan_impex.api import get_role_filter

@frappe.whitelist()
def my_customer_list():
    try:
        show_area_records = False
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
        if frappe.form_dict.get("show_area_records"):
            show_area_records = int(frappe.form_dict.get("show_area_records"))
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp, show_area_records)
        si_join = ""
        billing_query = ""
        if (frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date")) or frappe.form_dict.get("zero_billing"):
            one_year_ago = datetime.today() - timedelta(days=365)
            date_range = ">=" + one_year_ago.strftime("%Y-%m-%d")
            if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
                date_range = "BETWEEN '{0}' AND '{1}' ".format(frappe.form_dict["from_date"], frappe.form_dict["to_date"])
            billing_query = "si.docstatus = 1 AND"
            if isinstance(frappe.form_dict.get("zero_billing"), str):
                if int(frappe.form_dict["zero_billing"]):
                    billing_query = "(si.docstatus = 0 OR si.docstatus IS NULL) AND"
            si_join = """
                LEFT JOIN `tabSales Invoice` si 
                ON cu.name = si.customer 
                AND si.posting_date {date_range}
            """.format(date_range=date_range)
        query = """
            select cu.name, cu.customer_name, custom_shop_name as custom_shop, customer_primary_contact as contact, customer_primary_address as location, created_by_emp as created_by, workflow_state, COUNT(*) OVER() AS total_count
            from `tabCustomer` as cu
            join `tabDynamic Link` as dl on dl.link_name=cu.name
            {si_join}
            where {billing_query} {role_filter} and disabled=0 and customer_level="Primary" and kyc_status="Completed"
        """.format(si_join=si_join, billing_query=billing_query, role_filter=role_filter)
        group_by = " group by cu.name order by cu.creation desc "
        filter_checks = {
            "district": "district",
            "state": "state",
            "business_type": "business_type",
        }
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (cu.name LIKE "%{search_text}%" or cu.customer_name LIKE "%{search_text}%" or dl.parent LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += group_by
        query += pagination
        customer_info = frappe.db.sql(query, as_dict=True)
        for customer in customer_info:
            customer["location"] = customer["location"].rsplit('-', 1)[0] if customer["location"] else ""
            customer["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.my_customer.my_customer_form?name={customer['name']}"
        total_count = 0
        if customer_info:
            total_count = customer_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": customer_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "My Customer list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def my_customer_form():
    customer_name = frappe.form_dict.get("name")
    try:
        if not customer_name:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give Customer ID"
            return
        if not frappe.db.exists("Customer", customer_name):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give valid Customer ID"
            return
        cus_doc = frappe.get_doc("Customer", customer_name)
        cus_doc = frappe.get_value("Customer", {"name": customer_name}, ["name", "customer_name", "custom_shop_name as shop_name", "customer_primary_address", "customer_primary_contact"], as_dict=True)
        location = frappe.get_value("Address", {"name": cus_doc["customer_primary_address"]}, "address_title")
        contact = frappe.get_value("Contact", {"name": cus_doc["customer_primary_contact"]}, "first_name")
        cus_doc.pop("customer_primary_address")
        cus_doc.pop("customer_primary_contact")
        cus_doc["location"] = location
        cus_doc["contact"] = contact
        outstanding_amt = 0
        dash_info = get_dashboard_info("Customer", customer_name)
        if dash_info:
            outstanding_amt = dash_info[0].get("total_unpaid") or 0
        cus_doc["outstanding_amt"] = outstanding_amt
        cus_doc["last_billing_rate"] = frappe.get_value("Sales Invoice", {"customer": customer_name}, "grand_total") or 0
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "KYC form has been successfully fetched"
        frappe.local.response['data'] = [cus_doc]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def my_customer_ledger():
    # get_dashboard_info
    customer_name = frappe.form_dict.get("name")
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
        if not customer_name:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give Customer ID"
            return
        if not frappe.db.exists("Customer", customer_name):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give valid Customer ID"
            return
        
        si_query = """
           select name, posting_date as date, grand_total as amount, outstanding_amount as balance, creation, COUNT(*) OVER() AS total_count
           from `tabSales Invoice` as si
           where si.customer = "{customer_name}" and docstatus=1
        """.format(customer_name=customer_name)
        pe_query = """
           select name, posting_date as date, paid_amount as amount, difference_amount as balance, creation, COUNT(*) OVER() AS total_count
           from `tabPayment Entry` as pe
           where pe.payment_type = "Receive" and pe.party = "{customer_name}" and docstatus!=2
        """.format(customer_name=customer_name)
        if frappe.form_dict.get("search_text"):
            si_query += """ and (name LIKE "%{search_text}%" or outstanding_amount LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            pe_query += """ and (name LIKE "%{search_text}%" or difference_amount LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
        if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
            range_filter = """ and posting_date between "{0}" and "{1}" """.format(frappe.form_dict["from_date"], frappe.form_dict["to_date"])
            si_query += range_filter
            pe_query += range_filter
        si_query += pagination
        pe_query += pagination
        si_info = frappe.db.sql(si_query, as_dict=True)
        pe_info = frappe.db.sql(pe_query, as_dict=True)
        ledger_info = si_info + pe_info
        ledger_info = sorted(ledger_info, key=lambda x: x["creation"], reverse=True)
        total_count = 0
        if si_info:
            total_count += si_info[0]["total_count"]
        if pe_info:
            total_count += pe_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": ledger_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "My Customer Ledger has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"