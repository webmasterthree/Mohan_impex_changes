import frappe
from datetime import datetime
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
from mohan_impex.item_price import get_item_category_price
from frappe.model.workflow import apply_workflow
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import create_contact_number, get_address_text, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm
from frappe import _dict
from pprint import pprint
from erpnext.stock.get_item_details import get_item_details as erpnext_get_item_details
from erpnext.accounts.doctype.pricing_rule.pricing_rule import get_pricing_rule_for_item
from mohan_impex.api.auth import has_cp

@frappe.whitelist()
def so_list():
    try:
        tab = frappe.form_dict.get("tab")
        limit = frappe.form_dict.get("limit")
        is_self = frappe.form_dict.get("is_self")
        other_employee = frappe.form_dict.get("employee")
        current_page = frappe.form_dict.get("current_page")
        if not tab:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give the list tab"
            return
        if not limit or not current_page:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Either limit or current page is missing"
            return
        current_page = int(current_page)
        limit = int(limit)
        offset = limit * (current_page - 1)
        pagination = "limit %s offset %s"%(limit, offset)
        tab_filter = 'workflow_state = "%s"'%(tab)
        if tab != "Draft": #Submitted
            tab_filter = "workflow_state != 'Draft'"
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp, is_self, other_employee)
        is_self_filter = get_self_filter_status()
        order_by = " order by so.creation desc "
        query = """
            select name, shop_name, contact_number as contact, customer_address as location, workflow_state, COUNT(*) OVER() AS total_count
            from `tabSales Order` as so
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (so.customer_name LIKE "%{search_text}%" or so.shop_name LIKE "%{search_text}%" or so.contact_number LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
            and_filters.append("""so.transaction_date between "{0}" and "{1}" """.format(frappe.form_dict["from_date"], frappe.form_dict["to_date"]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        if frappe.form_dict.get("visit_type"):
            query += """ AND so.customer_level = "{0}" """.format(frappe.form_dict.get("visit_type"))
        query += order_by
        query += pagination
        so_info = frappe.db.sql(query, as_dict=True)
        for so in so_info:
            so["location"] = get_address_text(so["location"]) if so["location"] else ""
            so["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.sales_order.so_form?name={so['name']}"
        total_count = 0
        if so_info:
            total_count = so_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": so_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter,
                "create": has_create_perm("Sales Order")
            }
        ]
        # my_orders = list(filter(lambda d: d.get("workflow_state") != "Draft", so_list))
        # order_draft = list(filter(lambda d: d.get("workflow_state") == "Draft", so_list))
        # response = {
        #     "my_orders" : my_orders,
        #     "order_draft" : order_draft,
        #     "create_perm": False
        # }
        # if frappe.has_permission("Sales Order", "create"):
        #     response["create_perm"] = True
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sales Order list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def so_form():
    try:
        so_name = frappe.form_dict.get("name")
        if not so_name:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give Sales Order ID"
            return
        if not frappe.db.exists("Sales Order", so_name):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give valid Sales Order ID"
            return
        so_doc = frappe.get_doc("Sales Order", so_name)
        so_dict = {
            "name": so_doc.name,
            "doctype": so_doc.doctype,
            "customer_level": so_doc.customer_level,
            "customer": so_doc.customer,
            "customer_name": so_doc.customer_name,
            "shop": so_doc.shop,
            "shop_name": so_doc.shop_name,
            "delivery_date": so_doc.delivery_date,
            "channel_partner": so_doc.custom_channel_partner,
            "cp_name": so_doc.cp_name,
            "deal_type": so_doc.custom_deal_type,
            "location": so_doc.customer_address.rsplit('-', 1)[0] if so_doc.customer_address else "",
            "contact": so_doc.contact_number or "",
            "remarks": so_doc.remarks,
            "workflow_state": so_doc.workflow_state,
            "cust_edit_needed": so_doc.cust_edit_needed
        }
        items_by_template = {}

        for item in so_doc.items:
            item_dict = {
                "name": item.name,
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty
            }

            template = item.item_template
            if template in items_by_template:
                items_by_template[template]["items"].append(item_dict)
            else:
                items_by_template[template] = {
                    "item_template": template,
                    "items": [item_dict]
                }

        # Convert dictionary values to a list and update so_dict
        so_dict.update({"items": list(items_by_template.values())})
        activities = get_comments("Sales Order", so_dict["name"])
        so_dict["activities"] = activities
        is_self_filter = get_self_filter_status()
        so_dict["status_fields"] = get_workflow_statuses("Sales Order", so_name, get_session_emp_role())
        so_dict["has_toggle_filter"] = is_self_filter
        so_dict["created_person_mobile_no"] = frappe.get_value("Employee", so_dict.get("created_by_emp"), "custom_personal_mobile_number")

        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sales Order form has been successfully fetched"
        frappe.local.response['data'] = [so_dict]
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def create_so():
    try:
        frappe.db.begin()
        response = {}
        has_cp_app = has_cp()
        so_data = frappe.form_dict
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
            "created_by_emp": get_session_employee(),
            "territory": get_session_employee_area()
        }
        if has_cp_app:
            so_dict.update({
                "customer_level": so_data.get("customer_level"),
                "custom_channel_partner": so_data.get("channel_partner") or "",
                "cp_name": so_data.get("cp_name") or "",
            })
        # if so_data.get("channel_partner"):
        #     so_dict.update({"company": so_data.get("channel_partner")})
        payment_term = so_dict.get("payment_term")
        # payment_schedule = [{
        #    "payment_term": payment_term, 
        # }]
        # so_dict.update({"payment_schedule": payment_schedule})
        items = []
        for item in so_data.get("items"):
            rate = get_item_category_price(item.get("item_code"), item.get("item_category"))
            item_dict = {
                "item_template": item.get("item_template"),
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
                "qty": item.get("qty"),
                "uom": item.get("uom"),
                "rate": item.get("rate") or 0,
                "quote_custom_rate": item.get("quote_custom_rate") or 0, #This field type is check
                "quoted_rate": item.get("quoted_rate") or 0,
            }
            items.append(item_dict)
        if so_data.get("contact"):
            if not frappe.db.exists("Contact Number", so_data.get("contact")):
                create_contact_number(so_data.get("contact"), "Customer", so_data.get("customer"))
        so_dict.update({"items": items})
        if so_data.get("isupdate"):
            doc = frappe.get_doc("Sales Order", so_data.get("so_id"))
            doc.update(so_dict)
            doc.save()
        else:
            so_dict.update({"doctype": "Sales Order"})
            doc = frappe.get_doc(so_dict)
            doc.insert(ignore_mandatory=True)
        message = "Sales Order form has been successfully created as Draft"
        if so_data.action == "Submit":
            apply_workflow(doc, "Submit")
            message = "Sales Order form has been successfully submitted"
        response.update({
            "so_id": doc.name
        })
        frappe.local.response['status'] = True
        frappe.local.response['message'] = message
        frappe.local.response['data'] = [response]
        frappe.db.commit()
    except Exception as err:
        frappe.db.rollback()
        frappe.log_error("SO", frappe.get_traceback())
        # get_exception(err)

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

import json
@frappe.whitelist()
def get_item_details(item_code, uom, customer, warehouse):
    company = frappe.defaults.get_defaults().get("company") or None
    currency = frappe.defaults.get_defaults().get("currency") or None
    args = _dict({
        "doctype": "Sales Order",
        "company": company,
        "price_list": "Standard Selling",
        "customer": customer,
        "item_code": item_code,
        "qty": 1,
        "uom": uom,
        "currency":currency,
        "transaction_type": "Selling",
        "transaction_date": datetime.today().strftime('%Y-%m-%d'),
        "warehouse": warehouse,
        "condition": "custom_delivery_term == '50% payment required at the time of Deliverys' "
    })
    item_detail = erpnext_get_item_details(args)
    rate = item_detail.price_list_rate
    discount_percentage = item_detail.discount_percentage
    discount_amount = item_detail.discount_amount
    applied_discount_amount = 0
    pricing_rules = json.loads(item_detail.get("pricing_rules") or "[]")
    pricing_rule = ""
    if len(pricing_rules) > 0:
        pricing_rule = pricing_rules[0]
        rate_or_discount = frappe.get_value("Pricing Rule", pricing_rule, "rate_or_discount")
        if rate_or_discount == "Discount Percentage":
            applied_discount_amount = rate * discount_percentage / 100
        elif rate_or_discount == "Discount Amount":
            applied_discount_amount = discount_amount
    rate = rate - applied_discount_amount
    tax_percentage = frappe.get_value("Item Tax Template", item_detail.item_tax_template, "gst_rate") or 0 # GST DEPENDENT
    response = {
        "rate": rate,
        "pricing_rule": pricing_rule,
        "tax_percentage": tax_percentage
    }
    return response