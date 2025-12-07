import frappe
from datetime import datetime
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
from mohan_impex.item_price import get_item_category_price
from frappe.model.workflow import apply_workflow
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import create_contact_number, get_address_text, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm
from frappe import _dict
from erpnext.stock.get_item_details import get_item_details as erp_get_item_details
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
            "customer": so_doc.customer,
            "customer_name": so_doc.customer_name,
            "shop": so_doc.shop,
            "shop_name": so_doc.shop_name,
            "delivery_date": so_doc.delivery_date,
            "deal_type": so_doc.custom_deal_type,
            "location": so_doc.customer_address.rsplit('-', 1)[0] if so_doc.customer_address else "",
            "contact": so_doc.contact_number or "",
            "remarks": so_doc.remarks,
            "workflow_state": so_doc.workflow_state,
            "cust_edit_needed": so_doc.cust_edit_needed,
            "customer_visit": so_doc.customer_visit or "",
            "delivery_term": so_doc.custom_delivery_term or "",
            "warehouse": so_doc.set_warehouse,
        }
        if has_cp_app:
            so_dict.update({
                "customer_level": so_doc.customer_level,
                "channel_partner": so_doc.custom_channel_partner,
                "cp_name": so_doc.cp_name,
            })
        if so_doc.shipping_address_name:
            so_dict["shipping_address"] = frappe.db.get_values("Address", so_doc.shipping_address_name, ["name as shipping_address_name", "address_line1", "address_line2", "city", "district", "state", "pincode"], as_dict=1)
        if so_doc.customer_address:
            so_dict["billing_address"] = frappe.db.get_values("Address", so_doc.customer_address, ["name as billing_address_name", "address_line1", "address_line2", "city", "district", "state", "pincode"], as_dict=1)
        items_by_template = {}
        tax_total = 0
        item_total = 0
        for item in so_doc.items:
            tax_percentage = frappe.get_value("Item Tax Template", item.item_tax_template, "gst_rate") or 0
            tax_amount = item.amount * (tax_percentage / 100)
            tax_total += tax_amount
            item_total += item.amount
            item_dict = {
                "name": item.name,
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "uom": item.uom,
                "amount": item.amount,
                "rate": item.rate,
                "quote_custom_rate": item.quote_custom_rate or 0,
                "quoted_rate": item.quoted_rate or 0,
                "tax_percentage": tax_percentage, # GST DEPENDENT
                "tax_amount": tax_amount,
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
        so_dict["gst_total_amount"] = tax_total
        so_dict["item_total_amount"] = item_total
        so_dict["grand_total_amount"] = item_total + tax_total
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

# @frappe.whitelist()
# def create_so():
#     try:
#         frappe.db.begin()
#         response = {}
#         so_data = frappe.form_dict
#         so_dict = {
#             "customer": so_data.get("customer"),
#             "customer_name": so_data.get("customer_name"),
#             "custom_deal_type": so_data.get("deal_type"),
#             "shop": so_data.get("shop"),
#             "shop_name": so_data.get("shop_name"),
#             "customer_visit": so_data.get("customer_visit"),
#             "contact_number": so_data.get("contact"),
#             "delivery_date": so_data.get("delivery_date"),
#             "custom_delivery_term": so_data.get("delivery_term"),
#             "set_warehouse": so_data.get("warehouse"),
#             "remarks": so_data.get("remarks"),
#             "cust_edit_needed": so_data.get("cust_edit_needed"),
#             "shipping_address_name": so_data.get("shipping_address_name"),
#             "customer_address": so_data.get("billing_address_name"),
#             "created_by_emp": get_session_employee(),
#             "territory": get_session_employee_area()
#         }
#         if has_cp_app:
#             so_dict.update({
#                 "customer_level": so_data.get("customer_level"),
#                 "custom_channel_partner": so_data.get("channel_partner") or "",
#                 "cp_name": so_data.get("cp_name") or "",
#             })
#         # if so_data.get("channel_partner"):
#         #     so_dict.update({"company": so_data.get("channel_partner")})
#         payment_term = so_dict.get("payment_term")
#         # payment_schedule = [{
#         #    "payment_term": payment_term, 
#         # }]
#         # so_dict.update({"payment_schedule": payment_schedule})
#         items = []
#         for item in so_data.get("items"):
#             rate = get_item_category_price(item.get("item_code"), item.get("item_category"))
#             item_dict = {
#                 "item_template": item.get("item_template"),
#                 "item_code": item.get("item_code"),
#                 "item_name": item.get("item_name"),
#                 "qty": item.get("qty"),
#                 "uom": item.get("uom"),
#                 "rate": item.get("rate") or 0,
#                 "quote_custom_rate": item.get("quote_custom_rate") or 0, #This field type is check
#                 "quoted_rate": item.get("quoted_rate") or 0,
#             }
#             items.append(item_dict)
#         if so_data.get("contact"):
#             if not frappe.db.exists("Contact Number", so_data.get("contact")):
#                 create_contact_number(so_data.get("contact"), "Customer", so_data.get("customer"))
#         so_dict.update({"items": items})
#         if so_data.get("isupdate"):
#             doc = frappe.get_doc("Sales Order", so_data.get("so_id"))
#             doc.update(so_dict)
#             doc.save()
#         else:
#             so_dict.update({"doctype": "Sales Order"})
#             doc = frappe.get_doc(so_dict)
#             doc.insert(ignore_mandatory=True)
#         message = "Sales Order form has been successfully created as Draft"
#         if so_data.action == "Submit":
#             apply_workflow(doc, "Submit")
#             message = "Sales Order form has been successfully submitted"
#         response.update({
#             "so_id": doc.name
#         })
#         frappe.local.response['status'] = True
#         frappe.local.response['message'] = message
#         frappe.local.response['data'] = [response]
#         frappe.db.commit()
#     except Exception as err:
#         frappe.db.rollback()
#         frappe.log_error("SO", frappe.get_traceback())
#         # get_exception(err)

 
@frappe.whitelist()
def create_so():
    try:
        frappe.db.begin()
        response = {}
        so_data = frappe.form_dict

        # Decide target doctype per request
        is_cp = bool(has_cp())
        target_doctype = "Secondary Sales Order" if is_cp else "Sales Order"

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
            "created_by_emp": get_session_employee(),
            "territory": get_session_employee_area()
        }

        # CP-only extra fields (only if your target doctype has these fields)
        if is_cp:
            so_dict.update({
                "customer_level": so_data.get("customer_level"),
                "custom_channel_partner": so_data.get("channel_partner") or "",
                "cp_name": so_data.get("cp_name") or "",
            })

        items = []
        for item in (so_data.get("items") or []):
            # you compute rate but currently you are not using it; keep or use it as needed
            _rate = get_item_category_price(item.get("item_code"), item.get("item_category"))

            item_dict = {
                "item_template": item.get("item_template"),
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
                "qty": item.get("qty"),
                "uom": item.get("uom"),
                "rate": item.get("rate") or 0,
                "quote_custom_rate": item.get("quote_custom_rate") or 0,
                "quoted_rate": item.get("quoted_rate") or 0,
            }
            items.append(item_dict)

        if so_data.get("contact"):
            if not frappe.db.exists("Contact Number", so_data.get("contact")):
                create_contact_number(so_data.get("contact"), "Customer", so_data.get("customer"))

        so_dict.update({"items": items})

        # Update vs Create
        if so_data.get("isupdate"):
            docname = so_data.get("so_id")

            # If doctype passed by client, prefer it; else auto-detect where it exists
            dt = so_data.get("doctype")
            if not dt:
                if frappe.db.exists("Secondary Sales Order", docname):
                    dt = "Secondary Sales Order"
                elif frappe.db.exists("Sales Order", docname):
                    dt = "Sales Order"
                else:
                    frappe.throw(f"Document not found: {docname}")

            doc = frappe.get_doc(dt, docname)
            doc.update(so_dict)
            doc.save()
            target_doctype = dt  # keep response accurate
        else:
            so_dict.update({"doctype": target_doctype})
            doc = frappe.get_doc(so_dict)
            doc.insert(ignore_mandatory=True)

        message = f"{target_doctype} has been successfully created as Draft"
        if so_data.get("action") == "Submit":
            apply_workflow(doc, "Submit")
            message = f"{target_doctype} has been successfully submitted"

        response.update({"so_id": doc.name, "doctype": target_doctype})

        frappe.local.response["status"] = True
        frappe.local.response["message"] = message
        frappe.local.response["data"] = [response]

        frappe.db.commit()

    except Exception:
        frappe.db.rollback()
        frappe.log_error("CREATE_SO", frappe.get_traceback())
        frappe.local.response["status"] = False
        frappe.local.response["message"] = "Error while creating Sales Order"


















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

@frappe.whitelist()
def get_item_details():
    item_code = frappe.form_dict.get("item_code")
    customer = frappe.form_dict.get("customer")
    uom = frappe.form_dict.get("uom")
    warehouse = frappe.form_dict.get("warehouse")
    delivery_term = frappe.form_dict.get("delivery_term") or ""
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    qty = float(frappe.form_dict.get("qty") or 1)
    price_list = frappe.form_dict.get("price_list") or frappe.db.get_single_value("Selling Settings", "selling_price_list")

    frappe.set_user("Administrator")
    args = frappe._dict({
        "item_code": item_code,
        "customer": customer,
        "uom": uom,
        "warehouse": warehouse,
        "company": company,
        "price_list": price_list,
        "currency": "INR",
        "transaction_type": "selling",
        "doctype": "Sales Order",
        "items": [{"item_code": item_code, "qty": qty, "uom": uom}],
        "qty": qty
    })
    doc = frappe.new_doc("Sales Order")
    doc.custom_delivery_term = delivery_term

    item_details = erp_get_item_details(args, doc=doc, for_validate=True)

    pricing_rules_applied = json.loads(item_details.get("pricing_rules") or "[]")

    item_details = {
        "rate": item_details.get("price_list_rate"),
        "discount_percentage": item_details.get("discount_percentage"),
        "discount_amount": item_details.get("discount_amount"),
        "net_rate": item_details.get("net_rate"),
        "pricing_rules_applied": pricing_rules_applied,
        "free_items": item_details.get("free_item_data") or []
    }
    frappe.local.response['status'] = True
    frappe.local.response['data'] = item_details


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