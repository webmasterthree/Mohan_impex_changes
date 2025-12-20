import frappe
from datetime import datetime
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
from mohan_impex.item_price import get_item_category_price
from frappe.model.workflow import apply_workflow
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import create_contact_number, get_address_text, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm
from frappe import _dict
from mohan_impex.api.auth import has_cp
import json

has_cp_app = has_cp()


@frappe.whitelist()
def so_list():
    try:
        tab = frappe.form_dict.get("tab")
        limit = frappe.form_dict.get("limit")
        is_self = frappe.form_dict.get("is_self")
        other_employee = frappe.form_dict.get("employee")
        current_page = frappe.form_dict.get("current_page")

        if not tab:
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

        emp = frappe.get_value(
            "Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True
        )
        role_filter = get_role_filter(emp, is_self, other_employee)  # usually uses alias `so.`
        role_filter_so = role_filter
        role_filter_sso = role_filter.replace("so.", "sso.")

        is_self_filter = get_self_filter_status()

        if tab == "Draft":
            tab_filter_so = """so.workflow_state = "Draft" """
            tab_filter_sso = """sso.workflow_state = "Draft" """
        else:
            tab_filter_so = """so.workflow_state != "Draft" """
            tab_filter_sso = """sso.workflow_state != "Draft" """

        search_text = frappe.form_dict.get("search_text")
        from_date = frappe.form_dict.get("from_date")
        to_date = frappe.form_dict.get("to_date")
        visit_type = frappe.form_dict.get("visit_type")

        extra_so = ""
        extra_sso = ""

        if search_text:
            search_text = search_text.replace('"', '\\"')
            extra_so += f''' AND (so.customer_name LIKE "%{search_text}%" OR so.shop_name LIKE "%{search_text}%" OR so.contact_number LIKE "%{search_text}%") '''
            extra_sso += f''' AND (sso.customer_name LIKE "%{search_text}%" OR sso.shop_name LIKE "%{search_text}%" OR sso.contact_number LIKE "%{search_text}%") '''

        if from_date and to_date:
            extra_so += f''' AND (so.transaction_date BETWEEN "{from_date}" AND "{to_date}") '''
            extra_sso += f''' AND (sso.transaction_date BETWEEN "{from_date}" AND "{to_date}") '''

        if visit_type:
            extra_so += f''' AND so.customer_level = "{visit_type}" '''
            extra_sso += f''' AND sso.customer_level = "{visit_type}" '''

        sales_q = f"""
            SELECT
                so.name AS name,
                so.shop_name AS shop_name,
                so.contact_number AS contact,
                so.customer_address AS location,
                so.workflow_state AS workflow_state,
                so.creation AS creation,
                "Sales Order" AS doctype
            FROM `tabSales Order` so
            WHERE {tab_filter_so} AND {role_filter_so}
            {extra_so}
        """

        secondary_q = f"""
            SELECT
                sso.name AS name,
                sso.shop_name AS shop_name,
                sso.contact_number AS contact,
                sso.customer_address AS location,
                sso.workflow_state AS workflow_state,
                sso.creation AS creation,
                "Secondary Sales Order" AS doctype
            FROM `tabSecondary Sales Order` sso
            WHERE {tab_filter_sso} AND {role_filter_sso}
            {extra_sso}
        """

        query = f"""
            SELECT
                t.name,
                t.shop_name,
                t.contact,
                t.location,
                t.workflow_state,
                t.doctype,
                COUNT(*) OVER() AS total_count,
                t.creation
            FROM (
                {sales_q}
                UNION ALL
                {secondary_q}
            ) t
            ORDER BY t.creation DESC
            LIMIT {limit} OFFSET {offset}
        """

        so_info = frappe.db.sql(query, as_dict=True)

        base_url = frappe.utils.get_url()
        for row in so_info:
            row["location"] = get_address_text(row["location"]) if row.get("location") else ""
            row["form_url"] = (
                f"{base_url}/api/method/mohan_impex.api.sales_order.so_form"
                f"?doctype={row.get('doctype')}&name={row.get('name')}"
            )
            row.pop("creation", None)

        total_count = so_info[0]["total_count"] if so_info else 0
        page_count = math.ceil(total_count / int(limit)) if limit else 0

        response = [
            {
                "records": so_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter,
                "create": bool(has_create_perm("Sales Order") or has_create_perm("Secondary Sales Order")),
            }
        ]

        frappe.local.response["status"] = True
        frappe.local.response["message"] = "Sales Order list has been successfully fetched"
        frappe.local.response["data"] = response

    except Exception as err:
        get_exception(err)






import frappe

@frappe.whitelist()
def so_form():
	try:
		so_name = (frappe.form_dict.get("name") or "").strip()
		req_doctype = (frappe.form_dict.get("doctype") or "").strip()

		if not so_name:
			frappe.local.response["http_status_code"] = 404
			frappe.local.response["status"] = False
			frappe.local.response["message"] = "Please give Sales Order ID"
			return

		# Detect doctype safely
		dt = None
		if req_doctype in ("Sales Order", "Secondary Sales Order"):
			if frappe.db.exists(req_doctype, so_name):
				dt = req_doctype

		if not dt:
			if frappe.db.exists("Secondary Sales Order", so_name):
				dt = "Secondary Sales Order"
			elif frappe.db.exists("Sales Order", so_name):
				dt = "Sales Order"

		if not dt:
			frappe.local.response["http_status_code"] = 404
			frappe.local.response["status"] = False
			frappe.local.response["message"] = "Please give valid Sales Order ID"
			return

		so_doc = frappe.get_doc(dt, so_name)

		# -------------------------
		# Warehouse handling (UNCHANGED)
		# -------------------------
		warehouse = getattr(so_doc, "set_warehouse", "") or ""
		warehouse_name = ""

		if dt == "Secondary Sales Order":
			# Here: warehouse should be CP Warehouse docname like "CP-WAR-Delhi"
			if warehouse and frappe.db.exists("CP Warehouse", warehouse):
				warehouse_name = frappe.db.get_value("CP Warehouse", warehouse, "warehouse_name") or ""
			else:
				warehouse_name = ""
		else:
			# Here: warehouse should be Warehouse docname like "Goods In Transit - MI"
			if warehouse and frappe.db.exists("Warehouse", warehouse):
				warehouse_name = frappe.db.get_value("Warehouse", warehouse, "warehouse_name") or ""
			else:
				warehouse_name = ""

		# -------------------------
		# Payment Terms (NEW)
		# -------------------------
		payment_terms = getattr(so_doc, "payment_terms_template", "") or ""
		payment_terms_name = ""
		# Example: frappe.db.get_value("Payment Terms Template","10 Days","template_name")
		if payment_terms and frappe.db.exists("Payment Terms Template", payment_terms):
			payment_terms_name = (
				frappe.db.get_value("Payment Terms Template", payment_terms, "template_name") or ""
			)

		# -------------------------
		# Delivery Term (NEW)
		# -------------------------
		delivery_term = getattr(so_doc, "custom_delivery_term", "") or ""
		delivery_term_name = ""
		# Example: frappe.db.get_value("Delivery Term","ABC","delivery_term")
		if delivery_term and frappe.db.exists("Delivery Term", delivery_term):
			delivery_term_name = (
				frappe.db.get_value("Delivery Term", delivery_term, "delivery_term") or ""
			)

		so_dict = {
			"name": so_doc.name,
			"doctype": so_doc.doctype,
			"customer": so_doc.customer,
			"customer_name": so_doc.customer_name,
			"visit_type": getattr(so_doc, "customer_level", "") or "",
			"shop": getattr(so_doc, "shop", "") or "",
			"shop_name": getattr(so_doc, "shop_name", "") or "",
			"delivery_date": getattr(so_doc, "delivery_date", None),
			"deal_type": getattr(so_doc, "custom_deal_type", "") or "",
			"location": so_doc.customer_address.rsplit("-", 1)[0] if getattr(so_doc, "customer_address", None) else "",
			"contact": getattr(so_doc, "contact_number", "") or "",
			"remarks": getattr(so_doc, "remarks", "") or "",
			"workflow_state": getattr(so_doc, "workflow_state", "") or "",
			"cust_edit_needed": getattr(so_doc, "cust_edit_needed", 0) or 0,
			"customer_visit": getattr(so_doc, "customer_visit", "") or "",

			"warehouse": warehouse,
			"warehouse_name": warehouse_name,

			# Payment terms (code + name)
			"payment_terms": payment_terms,
			"payment_terms_name": payment_terms_name,

			# Delivery term (code + name)
			"delivery_term": delivery_term,
			"delivery_term_name": delivery_term_name,
		}

		if dt == "Secondary Sales Order":
			so_dict.update(
				{
					"customer_level": getattr(so_doc, "customer_level", "") or "",
					"channel_partner": getattr(so_doc, "custom_channel_partner", "") or "",
					"cp_name": getattr(so_doc, "cp_name", "") or "",
				}
			)

		# Shipping address
		if getattr(so_doc, "shipping_address_name", None):
			so_dict["shipping_address"] = frappe.db.get_values(
				"Address",
				so_doc.shipping_address_name,
				[
					"name as shipping_address_name",
					"address_line1",
					"address_line2",
					"city",
					"district",
					"state",
					"pincode",
				],
				as_dict=1,
			)

		# Billing address
		if getattr(so_doc, "customer_address", None):
			so_dict["billing_address"] = frappe.db.get_values(
				"Address",
				so_doc.customer_address,
				[
					"name as billing_address_name",
					"address_line1",
					"address_line2",
					"city",
					"district",
					"state",
					"pincode",
				],
				as_dict=1,
			)

		# Items + GST
		items_by_template = {}
		tax_total = 0
		item_total = 0

		for item in (so_doc.items or []):
			tax_percentage = frappe.get_value("Item Tax Template", item.item_tax_template, "gst_rate") or 0
			tax_amount = (item.amount or 0) * (tax_percentage / 100)

			tax_total += tax_amount
			item_total += (item.amount or 0)

			item_dict = {
				"name": item.name,
				"item_code": item.item_code,
				"item_name": item.item_name,
				"qty": item.qty,
				"uom": item.uom,
				"amount": item.amount,
				"rate": item.rate,
				"quote_custom_rate": getattr(item, "quote_custom_rate", 0) or 0,
				"quoted_rate": getattr(item, "quoted_rate", 0) or 0,
				"tax_percentage": tax_percentage,
				"tax_amount": tax_amount,
				"item_total": (item.amount or 0) + tax_amount,
			}

			template = getattr(item, "item_template", None) or "Default"
			if template in items_by_template:
				items_by_template[template]["items"].append(item_dict)
			else:
				items_by_template[template] = {"item_template": template, "items": [item_dict]}

		so_dict["items"] = list(items_by_template.values())
		so_dict["gst_total_amount"] = tax_total
		so_dict["item_total_amount"] = item_total
		so_dict["grand_total_amount"] = item_total + tax_total

		# Activities / workflow helpers
		so_dict["activities"] = get_comments(dt, so_doc.name)
		is_self_filter = get_self_filter_status()
		so_dict["status_fields"] = get_workflow_statuses(dt, so_name, get_session_emp_role())
		so_dict["has_toggle_filter"] = is_self_filter

		# Created by employee mobile
		created_by_emp = getattr(so_doc, "created_by_emp", None)
		if created_by_emp:
			so_dict["created_person_mobile_no"] = frappe.get_value(
				"Employee", created_by_emp, "custom_personal_mobile_number"
			) or ""
		else:
			so_dict["created_person_mobile_no"] = ""

		frappe.local.response["status"] = True
		frappe.local.response["message"] = "Sales Order form has been successfully fetched"
		frappe.local.response["data"] = [so_dict]

	except Exception as err:
		get_exception(err)



from frappe import _

@frappe.whitelist()
def create_so():
	try:
		frappe.db.begin()

		so_data = frappe._dict(frappe.form_dict or {})
		response = {}

		is_cp = bool(has_cp())
		customer_level = (so_data.get("customer_level") or "").strip()

		if not is_cp:
			customer_level = "Primary"
			target_doctype = "Sales Order"
		else:
			if customer_level == "Secondary":
				target_doctype = "Secondary Sales Order"
			elif customer_level == "Primary":
				target_doctype = "Sales Order"
			else:
				frappe.throw(_("Invalid customer_level. Allowed values: Primary, Secondary"))

		so_dict = {
			"customer": so_data.get("customer"),
			"customer_name": so_data.get("customer_name"),
			"custom_deal_type": so_data.get("deal_type"),
			"shop": so_data.get("shop"),
			"shop_name": so_data.get("shop_name"),
			"customer_visit": so_data.get("customer_visit"),
			"contact_number": so_data.get("contact"),
			"delivery_date": so_data.get("delivery_date"),
			"custom_delivery_term": so_data.get("delivery_term"),
			"set_warehouse": so_data.get("warehouse"),
			"remarks": so_data.get("remarks"),
			"cust_edit_needed": so_data.get("cust_edit_needed"),
			"shipping_address_name": so_data.get("shipping_address_name"),
			"customer_address": so_data.get("billing_address_name"),
			"payment_terms_template": so_data.get("payment_terms_template"),
			"created_by_emp": get_session_employee(),
			"territory": get_session_employee_area(),
			"customer_level": customer_level,
			"channel_partner": so_data.get("custom_channel_partner") or "",
			"channel_partner_name": so_data.get("cp_name") or "",
		}

		if target_doctype == "Secondary Sales Order":
			so_dict.update({
				"custom_channel_partner": so_data.get("channel_partner") or "",
				"cp_name": so_data.get("cp_name") or "",
			})

		items_data = so_data.get("items") or []
		if isinstance(items_data, str):
			items_data = frappe.parse_json(items_data)

		items = []
		for row in (items_data or []):
			row = frappe._dict(row or {})
			items.append({
				"item_template": row.get("item_template"),
				"item_code": row.get("item_code"),
				"item_name": row.get("item_name"),
				"qty": row.get("qty"),
				"uom": row.get("uom"),
				"rate": row.get("rate") or 0,
				"amount": row.get("amount"),
				"quote_custom_rate": row.get("quote_custom_rate") or 0,
				"quoted_rate": row.get("quoted_rate") or 0,
			})

		so_dict["items"] = items

		contact = (so_data.get("contact") or "").strip()
		if contact:
			if not frappe.db.exists("Contact Number", contact):
				create_contact_number(contact, "Customer", so_data.get("customer"))

		isupdate = so_data.get("isupdate")
		if isinstance(isupdate, str):
			isupdate = isupdate.strip().lower() in ("1", "true", "yes", "y")
		else:
			isupdate = bool(isupdate)

		if isupdate:
			docname = so_data.get("so_id")
			if not docname:
				frappe.throw(_("Missing so_id for update"))

			if frappe.db.exists("Secondary Sales Order", docname):
				dt = "Secondary Sales Order"
			elif frappe.db.exists("Sales Order", docname):
				dt = "Sales Order"
			else:
				frappe.throw(_("Document not found: {0}").format(docname))

			doc = frappe.get_doc(dt, docname)
			doc.update(so_dict)
			doc.save(ignore_permissions=True)
			target_doctype = dt
		else:
			so_dict["doctype"] = target_doctype
			doc = frappe.get_doc(so_dict)
			doc.insert(ignore_mandatory=True, ignore_permissions=True)

		message = f"{target_doctype} has been successfully created as Draft"
		if (so_data.get("action") or "").strip() == "Submit":
			apply_workflow(doc, "Submit")
			message = f"{target_doctype} has been successfully submitted"

		response.update({"so_id": doc.name, "doctype": target_doctype})

		frappe.local.response["status"] = True
		frappe.local.response["message"] = message
		frappe.local.response["data"] = [response]

		frappe.db.commit()

	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "CREATE_SO")

		frappe.local.response["status"] = False
		frappe.local.response["message"] = str(e) if str(e) else "Error while creating Sales Order"
		frappe.local.response["data"] = []
		frappe.local.response["http_status_code"] = 400



def get_role_filter(emp, is_self=None, employee=None):
    from frappe.utils.nestedset import get_descendants_of
    territory_list = set(frappe.get_all("User Permission", {"allow": "Territory", "user": emp.get("user_id")}, ["for_value as area"], pluck="area"))
    consolidated_territory = set(territory_list)
    for area in territory_list:
        consolidated_territory.update(get_descendants_of("Territory", area))
    areas = "', '".join(consolidated_territory) if consolidated_territory else f"""{emp.get("area")}"""
    if employee:
        return f"""territory in ('{areas}') and created_by_emp = '{employee}' """
    if is_self is not None:
        if int(is_self) == 1:
            return f"""territory in ('{areas}') and created_by_emp = '{emp.get('name')}' """
        elif int(is_self) == 0:
            return f"""territory in ('{areas}') and (created_by_emp != '{emp.get('name')}' or created_by_emp is null) """
    return f"""territory in ('{areas}') """

@frappe.whitelist()
def get_addresses(customer, address_type):
    try:
        query = """
            select a.name, a.address_title, a.address_line1, a.address_line2, a.city, a.district, a.state, a.pincode
            from `tabAddress` a
            inner join `tabDynamic Link` b on a.name = b.parent
            where 
                b.link_doctype = 'Customer' and b.link_name = "{customer}" and a.address_type = "{address_type}" and
                b.parenttype = 'Address' and b.parentfield = 'links'
        """.format(customer=customer, address_type=address_type)
        address_list = frappe.db.sql(query, as_dict=1)
        for address in address_list:
            address["city_name"] = frappe.db.get_value("City", address["city"], "city") or address["city"]
            address["district_name"] = frappe.db.get_value("District", address["district"], "district") or address["district"]
            address["state_name"] = frappe.db.get_value("State", address["state"], "state") or address["state"]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"{address_type} addresses have been successfully fetched"
        frappe.local.response['data'] = address_list
    except Exception as err:
        get_exception(err)


@frappe.whitelist()
def get_warehouses():
    try:
        company = frappe.defaults.get_defaults().get("company") or None
        warehouses = frappe.get_all("Warehouse", {"disabled": "0", "company": company}, ["name", "warehouse_name"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Warehouses list has been successfully fetched"
        frappe.local.response['data'] = warehouses
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def calculate_item_tax(item_code, qty=1, rate=0):

    company = frappe.db.get_single_value("Global Defaults", "default_company")
    tax_template = frappe.get_value("Sales Taxes and Charges Template", {"company": company, "is_default": 1}, "name")
    if not tax_template:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Default Sales Taxes and Charges Template not found"
        return
    so = frappe.new_doc("Sales Order")
    so.company = company
    so.currency = frappe.db.get_value("Company", company, "default_currency")
    so.taxes_and_charges = tax_template
    # Add item row
    item = so.append("items", {
        "item_code": item_code,
        "qty": qty,
        "rate": rate
    })

    # Load Tax Template Rows
    so.set("taxes", [])
    template_taxes = frappe.get_all(
        "Sales Taxes and Charges",
        filters={"parent": tax_template},
        fields=["*"]
    )
    for row in template_taxes:
        so.append("taxes", row)

    # Recalculate totals
    so.set_missing_values()
    so.calculate_taxes_and_totals()

    tax_rate = 0
    tax_amount = 0
    total_amount = 0
    for tax_row in so.taxes:
        if not tax_row.item_wise_tax_detail:
            continue
        item_wise = frappe.parse_json(tax_row.item_wise_tax_detail)
        
        if len(item_wise.keys()) == 1:
            item_code = list(item_wise.keys())[0]
            tax_info = item_wise[item_code]
            # tax_info can be: 18.0 or [18.0, 1800.0]
            if isinstance(tax_info, list):
                tax_rate = tax_info[0]
                tax_amount = tax_info[1]
            else:
                tax_rate = tax_row.rate
                tax_amount = tax_info

    total_amount = item.net_amount + tax_amount
    item_tax_info = {
        "item_code": item_code,
        "qty": qty,
        "rate": rate,
        "uom": item.uom,
        "item_net_amount": item.net_amount,
        "item_tax_rate": tax_rate,
        "item_tax_amount": tax_amount,
        "item_total_amount": total_amount
    }
    frappe.local.response['status'] = True
    frappe.local.response['data'] = item_tax_info

@frappe.whitelist()
def get_tag_list(customer, search_text=""):
    tag_list = frappe.db.sql_list("""
        SELECT DISTINCT cvm.name 
        FROM `tabCustomer Visit Management` cvm
        LEFT JOIN `tabUnverified Customer` uc ON cvm.unv_customer = uc.name
        WHERE (cvm.customer = %s OR uc.customer = %s)
        """ + (f"AND cvm.name LIKE %s" if search_text else ""),
        (customer, customer) + ((f"%{search_text}%",) if search_text else ())
    )
    frappe.local.response['status'] = True
    frappe.local.response['data'] = tag_list