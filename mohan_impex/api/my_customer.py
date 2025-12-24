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
		tab = frappe.form_dict.get("tab")
		limit = frappe.form_dict.get("limit")
		current_page = frappe.form_dict.get("current_page")
		is_self = frappe.form_dict.get("is_self")
		other_employee = frappe.form_dict.get("employee")

		if has_cp() and not tab:
			frappe.local.response["http_status_code"] = 404
			frappe.local.response["status"] = False
			frappe.local.response["message"] = "Please give the list tab"
			return

		if not limit or not current_page:
			frappe.local.response["http_status_code"] = 404
			frappe.local.response["status"] = False
			frappe.local.response["message"] = "Either limit or current page is missing"
			return

		current_page = int(current_page)
		limit = int(limit)
		offset = limit * (current_page - 1)
		pagination = "limit %s offset %s" % (limit, offset)

		emp = frappe.get_value(
			"Employee",
			{"user_id": frappe.session.user},
			["name", "area", "user_id"],
			as_dict=True
		)

		role_filter = get_role_filter(emp, is_self, other_employee)
		is_self_filter = get_self_filter_status()

		si_join = ""
		billing_query = ""

		if (frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date")) or frappe.form_dict.get("zero_billing"):
			one_year_ago = datetime.today() - timedelta(days=365)
			date_range = ">=" + one_year_ago.strftime("%Y-%m-%d")

			if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
				date_range = "BETWEEN '{0}' AND '{1}' ".format(frappe.form_dict["from_date"], frappe.form_dict["to_date"])

			billing_query = "si.docstatus = 1 AND"

			if frappe.form_dict.get("zero_billing"):
				if isinstance(frappe.form_dict.get("zero_billing"), str):
					if int(frappe.form_dict.get("zero_billing")):
						billing_query = "(si.docstatus = 0 OR si.docstatus IS NULL) AND"

			si_join = """
				LEFT JOIN `tabSales Invoice` si
				ON cu.name = si.customer
				AND si.posting_date {date_range}
			""".format(date_range=date_range)

		# ✅ UPDATED: fetch contact from Contact Number via Dynamic Link (parenttype="Contact Number", parentfield="links")
		# Picks latest created Contact Number linked to that Customer
		query = """
			SELECT
				cu.name,
				cu.customer_name,
				cu.custom_shop_name AS custom_shop,
				(
					SELECT cn.contact_number
					FROM `tabDynamic Link` dl2
					INNER JOIN `tabContact Number` cn
						ON cn.name = dl2.parent
					WHERE dl2.link_doctype = 'Customer'
						AND dl2.link_name = cu.name
						AND dl2.parenttype = 'Contact Number'
						AND dl2.parentfield = 'links'
					ORDER BY cn.creation DESC
					LIMIT 1
				) AS contact,
				cu.customer_primary_address AS location,
				cu.workflow_state,
				cu.created_by_emp,
				cu.created_by_name,
				COUNT(*) OVER() AS total_count
			FROM `tabCustomer` AS cu
			LEFT JOIN `tabDynamic Link` AS dl ON dl.link_name = cu.name
			LEFT JOIN `tabCustomer Consumption Info` AS cci ON cci.parent = cu.name
			{si_join}
			WHERE {billing_query} {role_filter}
				AND cu.disabled = 0
				AND cu.kyc_status = "Completed"
		""".format(si_join=si_join, billing_query=billing_query, role_filter=role_filter)

		group_by = " GROUP BY cu.name ORDER BY cu.creation DESC "

		filter_checks = {
			"city": "city",
			"district": "district",
			"state": "state",
			"business_type": "business_type",
		}

		if frappe.form_dict.get("category_type"):
			query += """ AND cci.category_type = "{category_type}" """.format(
				category_type=frappe.form_dict.get("category_type")
			)

		if frappe.form_dict.get("segment"):
			query += """ AND cci.segment = "{segment}" """.format(
				segment=frappe.form_dict.get("segment")
			)

		if tab:
			query += f""" AND cu.customer_level = "{tab}" """

		if frappe.form_dict.get("search_text"):
			or_filters = """
				AND (
					cu.name LIKE "%{search_text}%"
					OR cu.customer_name LIKE "%{search_text}%"
					OR (dl.parent LIKE "%{search_text}%" AND dl.parenttype = "Contact Number")
				)
			""".format(search_text=frappe.form_dict.get("search_text"))
			query += or_filters

		and_filters = []
		for key, value in filter_checks.items():
			if frappe.form_dict.get(key):
				and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))

		and_filters = " AND ".join(and_filters)
		query += """ AND ({0})""".format(and_filters) if and_filters else ""

		query += group_by
		query += pagination

		frappe.log_error(query, "Query")

		customer_info = frappe.db.sql(query, as_dict=True)

		for customer in customer_info:
			customer["location"] = frappe.get_value(
				"Address",
				{"name": customer["location"]},
				["name", "address_title", "address_line1", "address_line2", "city", "state", "pincode"],
				as_dict=True
			) if customer.get("location") else ""

			customer["form_url"] = (
				f"{frappe.utils.get_url()}/api/method/mohan_impex.api.my_customer.my_customer_form?name={customer['name']}"
			)

		total_count = 0
		if customer_info:
			total_count = customer_info[0].get("total_count") or 0

		page_count = math.ceil(total_count / int(limit)) if int(limit) else 0

		response = [
			{
				"records": customer_info,
				"total_count": total_count,
				"page_count": page_count,
				"current_page": current_page,
				"has_toggle_filter": is_self_filter
			}
		]

		frappe.local.response["status"] = True
		frappe.local.response["message"] = "My Customer list has been successfully fetched"
		frappe.local.response["data"] = response

	except Exception as err:
		get_exception(err)

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
        fields = ["name", "customer_name", "customer_type as company_type", "email_id", "custom_shop_name as shop_name", "customer_primary_address", "mobile_no", "business_type", "pan", "gstin", "proposed_credit"]
        if has_cp():
            fields.append("is_dl")
            fields.append("customer_level")
            fields.append("custom_channel_partner")
            fields.append("cp_name")
        cus_doc = frappe.get_value("Customer", {"name": customer_name}, fields, as_dict=True)
        # location = frappe.get_all("Address", {"name": cus_doc["customer_primary_address"]}, ["name","address_title", "address_line1", "address_line2", "city", "state", "pincode"], as_dict=True)
        billing_address_list = []
        shipping_address_list = []
        query = """
            select a.name, a.address_type, a.address_title, a.address_line1, a.address_line2, a.city, a.district, a.state, a.pincode
            from `tabDynamic Link` dl
            inner join `tabAddress` a on dl.parent = a.name
            where dl.link_name = "{customer_name}" and dl.link_doctype = "Customer" and dl.parenttype = "Address"
        """.format(customer_name=customer_name)
        dynamic_link_list = frappe.db.sql(query, as_dict=True)
        if has_cp():
            if cus_doc.get("customer_level") == "Primary":
                cus_doc["customer_type"] = "DL" if cus_doc.get("is_dl") else "DP"
                cus_doc.pop("is_dl")
                get_default_customer_info(cus_doc, customer_name)
            elif cus_doc.get("customer_level") == "Secondary":
                cus_doc.pop("company_type")
                cus_doc.pop("email_id")
                cus_doc.pop("gstin")
                cus_doc.pop("business_type")
                cus_doc.pop("pan")
                cus_doc.pop("proposed_credit")
        else:
            get_default_customer_info(cus_doc, customer_name)
        for dl in dynamic_link_list:
            if dl["address_type"] == "Billing":
                billing_address_list.append(dl)
            elif dl["address_type"] == "Shipping":
                shipping_address_list.append(dl)
        cus_doc["billing_address_list"] = billing_address_list
        cus_doc["shipping_address_list"] = shipping_address_list
        cus_doc.pop("customer_primary_address")
        # cus_doc["location"] = location
        cus_doc["consumption_info"] = get_customer_segment_info(cus_doc["name"])
        cus_doc["change_requests"] = get_change_request(cus_doc["name"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "KYC form has been successfully fetched"
        frappe.local.response['data'] = [cus_doc]
    except Exception as err:
        get_exception(err)

def get_default_customer_info(cus_doc, customer_name):
    outstanding_amt = 0
    dash_info = get_dashboard_info("Customer", customer_name)
    if dash_info:
        outstanding_amt = dash_info[0].get("total_unpaid") or 0
    cus_doc["contact"] = cus_doc.mobile_no or ""
    cus_doc["credit_days"], cus_doc["credit_limit"] = get_credit_days_and_limit(cus_doc["name"])
    cus_doc["outstanding_amt"] = abs(outstanding_amt)
    cus_doc["last_billing_rate"] = frappe.get_value("Sales Invoice", {"customer": customer_name}, "grand_total") or 0

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
        get_exception(err)

@frappe.whitelist()
def add_change_request(customer_id, requested_content):
    try:
        customer_doc = frappe.get_doc("Customer", customer_id)
        row = customer_doc.append("change_request", {
            "requested_content": requested_content
        })
        customer_doc.save()
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Change Request has been successfully created"
    except Exception as err:
        # get_exception(err)
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"{err}"

@frappe.whitelist()
def get_change_request(customer_id):
    change_request = frappe.db.get_all("Change Request", {"parent": customer_id, "parenttype": "Customer", "parentfield": "change_request"}, ["requested_content", "status"])
    return change_request

def get_customer_segment_info(customer_id):
    consumption_info = frappe.db.get_all("Customer Consumption Info", {"parent": customer_id, "parenttype": "Customer", "parentfield": "customer_consumption_info"}, ["segment", "product_name", "category_type", "consumption_qty", "uom"])
    return consumption_info

def get_credit_days_and_limit(customer_id):
    company = frappe.defaults.get_defaults().get("company")
    credit_limit_doc = frappe.db.get_value("Customer Credit Limit", {"company": company, "parent": customer_id}, ["credit_days", "credit_limit"])
    if credit_limit_doc:
        credit_days, credit_limit = credit_limit_doc
    else:
        credit_days = 0
        credit_limit = 0
    return credit_days, credit_limit
