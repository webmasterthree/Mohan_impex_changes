import frappe
from datetime import datetime
from mohan_impex.mohan_impex.utils import get_session_employee
from mohan_impex.item_price import get_item_category_price
from frappe.model.workflow import apply_workflow
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import create_contact

@frappe.whitelist()
def so_list():
    try:
        show_area_records = False
        tab = frappe.form_dict.get("tab")
        limit = frappe.form_dict.get("limit")
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
        if tab != "Draft":
            tab_filter = "workflow_state != 'Draft'"
        if frappe.form_dict.get("show_area_records"):
            show_area_records = int(frappe.form_dict.get("show_area_records"))
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp, show_area_records)
        order_by = " order by so.creation desc "
        query = """
            select name, shop_name, contact_person as contact, customer_address as location, created_by_emp as created_by, workflow_state, COUNT(*) OVER() AS total_count
            from `tabSales Order` as so
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (so.customer_name LIKE "%{search_text}%" or so.shop_name LIKE "%{search_text}%" or so.contact_person LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
            and_filters.append("""so.transaction_date between "{0}" and "{1}" """.format(frappe.form_dict["from_date"], frappe.form_dict["to_date"]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_by
        query += pagination
        so_info = frappe.db.sql(query, as_dict=True)
        # so_info = frappe.get_list("Sales Order", role_filter, ["name", "custom_shop_name", "contact_person as contact", "shipping_address_name as location", "created_by_emp as created_by", "workflow_state"])
        for so in so_info:
            so["location"] = so["location"].rsplit('-', 1)[0] if so["location"] else ""
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
                "current_page": current_page
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
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

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
            "customer_level": so_doc.customer_level,
            "customer": so_doc.customer,
            "customer_name": so_doc.customer_name,
            "shop": so_doc.shop,
            "shop_name": so_doc.shop_name,
            "delivery_date": so_doc.delivery_date,
            "channel_partner": so_doc.custom_channel_partner,
            "deal_type": so_doc.custom_deal_type,
            "location": so_doc.customer_address.rsplit('-', 1)[0] if so_doc.customer_address else "",
            "contact": so_doc.contact_person or "",
            "remarks": so_doc.remarks,
            "workflow_state": so_doc.workflow_state
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
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sales Order form has been successfully fetched"
        frappe.local.response['data'] = [so_dict]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def create_so():
    try:
        response = {}
        so_data = frappe.form_dict
        so_dict = {
            "customer_level": so_data.get("customer_level"),
            "custom_channel_partner": so_data.get("channel_partner") or "",
            "customer": so_data.get("customer"),
            "customer_name": so_data.get("customer_name"),
            "custom_deal_type": so_data.get("deal_type"),
            "shop": so_data.get("shop"),
            "shop_name": so_data.get("shop_name"),
            "contact_person": so_data.get("contact"),
            "delivery_date": so_data.get("delivery_date"),
            "remarks": so_data.get("remarks"),
            "cust_edit_needed": so_data.get("cust_edit_needed"),
            "created_by_emp": get_session_employee()
        }
        if so_data.get("channel_partner"):
            so_dict.update({"company": so_data.get("channel_partner")})
        items = []
        for item in so_data.get("items"):
            rate = get_item_category_price(item.get("item_code"), item.get("item_category"))
            item_dict = {
                "item_template": item.get("item_template"),
                "item_code": item.get("item_code"),
                "item_name": item.get("item_name"),
                "qty": item.get("qty"),
                "rate": rate
            }
            items.append(item_dict)
        if so_data.get("contact"):
            if not frappe.db.exists("Contact", so_data.get("contact")):
                create_contact(so_data.get("contact"), "Customer", so_data.get("customer"))
        so_dict.update({"items": items})
        if so_data.get("isupdate"):
            doc = frappe.get_doc("Sales Order", so_data.get("so_id"))
            doc.update(so_dict)
            doc.save()
        else:
            so_dict.update({"doctype": "Sales Order"})
            doc = frappe.get_doc(so_dict)
            doc.insert()
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
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

def get_role_filter(emp, show_area_records):
    from frappe.utils.nestedset import get_descendants_of
    if show_area_records:
        sub_areas = get_descendants_of("Territory", emp.get('area'))
        if sub_areas:
            sub_areas.append(emp.get('area'))
            areas = "', '".join(sub_areas)
        else:
            areas = f"""{emp.get("area")}"""
        return f"""territory in ('{areas}') """
    return f"""created_by_emp = "{emp.get('name')}" """