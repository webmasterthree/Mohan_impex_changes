import frappe
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee
import math
from mohan_impex.api import get_signed_token
from mohan_impex.api.sales_order import get_role_filter
from datetime import datetime
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import create_contact_number, get_self_filter_status
from mohan_impex.mohan_impex.contact import get_contact_numbers

@frappe.whitelist()
def kyc_list():
    try:
        tab = frappe.form_dict.get("tab")
        limit = frappe.form_dict.get("limit")
        is_self = int(frappe.form_dict.get("is_self") or 0)
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
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area", "role_profile"], as_dict=True)
        role_filter = get_role_filter(emp, is_self, other_employee)
        is_self_filter = get_self_filter_status()
        order_and_group_by = " group by cu.name order by cu.creation desc "
        query = """
            select cu.name, cu.customer_name, cu.request_date as created_date, IF(workflow_state='KYC Pending', cu.request_date, IF(workflow_state='KYC Completed', cu.kyc_complete_date, cu.request_date)) AS status_date, cu.workflow_state, cu.created_by_emp, cu.created_by_name, COUNT(*) OVER() AS total_count
            from `tabCustomer` as cu
            JOIN `tabDynamic Link` as dl on dl.link_name = cu.name
            where customer_level= "Primary" and dl.parenttype = "Contact Number" and {tab_filter} and {role_filter}
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "customer_type": "customer_type",
            "business_type": "business_type",
            "segment": "market_segment",
            "customer_category": "custom_customer_category"
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
        query += order_and_group_by
        query += pagination
        kyc_info = frappe.db.sql(query, as_dict=True)
        for kyc in kyc_info:
            kyc["workflow_state"] = "Approved" if kyc["workflow_state"] == "KYC Completed" else "Pending"
            kyc["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.kyc.kyc_form?name={kyc['name']}"
            kyc.pop("created_by_emp", None)
        total_count = 0
        if kyc_info:
            total_count = kyc_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": kyc_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "KYC request list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def kyc_form():
    kyc_name = frappe.form_dict.get("name")
    try:
        if not kyc_name:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give KYC ID"
            return
        if not frappe.db.exists("Customer", kyc_name):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give valid KYC ID"
            return
        kyc_doc = frappe.get_doc("Customer", kyc_name)
        kyc_doc = kyc_doc.as_dict()
        fields_to_remove = ["owner", "creation", "modified", "modified_by", "docstatus", "idx", "amended_from", "doctype", "parent", "parenttype", "parentfield", "territory"]
        child_doc = ["product_pitching", "product_trial", "customer_license", "cust_decl"]
        kyc_doc = {
            key: value for key, value in kyc_doc.items() if key not in fields_to_remove
        }
        for child_name in child_doc:
            if child_name in kyc_doc:
                kyc_doc[child_name] = [
                    {k: v for k, v in item.items() if k not in fields_to_remove}
                    for item in kyc_doc[child_name]
                ]
        for license in kyc_doc.get("customer_license"):
            license["cust_lic"] = get_signed_token(license["cust_lic"])
        for decl in kyc_doc.get("cust_decl"):
            decl["cust_decl"] = get_signed_token(decl["cust_decl"])
        address_types = [
            {
                "type": "Billing",
                "prefer": "is_primary_address",
                "field_name": "billing_address"
            },
            {
                "type": "Shipping",
                "prefer": "is_shipping_address",
                "field_name": "shipping_address"
            }
        ]
        for address_type in address_types:
            address_query = f"""
                select ad.name as address, address_title, address_line1, address_line2, city, state, country, pincode
                from `tabAddress` ad
                join `tabDynamic Link` dl on ad.name = dl.parent
                where dl.link_name = "{kyc_name}" and ad.address_type = "{address_type['type']}" and {address_type['prefer']} = 1 limit 1
            """
            address = frappe.db.sql(address_query, as_dict=True)
            kyc_doc[address_type["field_name"]] = address
        # contact_query = f"""
        #     select con.name
        #     from `tabContact Number` con
        #     join `tabDynamic Link` dl on con.name = dl.parent
        #     where dl.link_name = "{kyc_name}" limit 1
        # """
        # contact = frappe.db.sql_list(contact_query)
        contact = frappe.get_value("Contact", {"name": kyc_doc["customer_primary_contact"]}, "mobile_no")
        activities = get_comments("Customer", kyc_doc["name"])
        kyc_doc["activities"] = activities
        kyc_doc["contact"] = [contact] if contact else []
        is_self_filter = get_self_filter_status()
        kyc_doc["has_toggle_filter"] = is_self_filter
        kyc_doc["created_person_mobile_no"] = frappe.get_value("Employee", kyc_doc.get("created_by_emp"), "custom_personal_mobile_number")
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "KYC form has been successfully fetched"
        frappe.local.response['data'] = [kyc_doc]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def create_kyc():
    kyc_data = frappe.form_dict
    kyc_data.pop("cmd")
    try:
        cust_decls = [{"cust_decl": cust_decl["file_url"]} for cust_decl in kyc_data.cust_decl]
        cust_licenses = [{"cust_lic": cust_license["file_url"]} for cust_license in kyc_data.cust_license]
        data = {
            "unv_customer": kyc_data.unv_customer,
            "created_by_emp": get_session_employee(),
            "territory": get_session_employee_area(),
            "customer_name": kyc_data.customer_name,
            "customer_type": kyc_data.customer_type,
            "customer_level": kyc_data.customer_level,
            "business_type": kyc_data.business_type,
            "custom_shop": kyc_data.shop,
            "custom_shop_name": kyc_data.shop_name,
            "gstin": kyc_data.gst_no,
            "district": kyc_data.district,
            "state": kyc_data.state,
            "request_date": datetime.today(),
            "market_segment": kyc_data.segment,
            "pan": kyc_data.pan,
            "cust_decl": cust_decls,
            "customer_license": cust_licenses,
            "email_id": kyc_data.email_id,
            "customer_details": kyc_data.remarks
        }
        data.update({"doctype": "Customer"})
        kyc_doc = frappe.get_doc(data)
        kyc_doc.insert()
        for cust_decl in kyc_data.cust_decl:
            update_file_doc(cust_decl.get("name"), kyc_doc.name)
        for cust_license in kyc_data.cust_license:
            update_file_doc(cust_license.get("name"), kyc_doc.name)
        contact_num_doc = create_contact_number(kyc_data["contact"], "Customer", kyc_doc.name)
        contact = create_contact(kyc_doc, kyc_data, contact_num_doc.name)
        billing_address = create_address(kyc_doc, kyc_data["billing_address"], "Billing")
        shipping_address = create_address(kyc_doc, kyc_data["shipping_address"], "Shipping")
        frappe.db.set_value('Customer', kyc_doc.name, 'customer_primary_address', billing_address)
        frappe.db.set_value('Customer', kyc_doc.name, 'customer_primary_contact', contact)
        frappe.db.set_value("Customer", kyc_doc.name, "mobile_no", kyc_data.contact)
        response = {
            "kyc": kyc_doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "KYC request has been successfully created"
        frappe.local.response['data'] = [response]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

def update_file_doc(name, kyc_id):
    doc = frappe.get_doc("File", name)
    doc.attached_to_doctype = "Customer"
    doc.attached_to_name = kyc_id
    doc.save()

def create_contact(kyc_doc, kyc_data, primary_contact_number):
    if kyc_doc.customer_primary_contact:
        contact_doc = frappe.get_doc("Contact", kyc_doc.customer_primary_contact)
    else:
        contact_doc = frappe.new_doc("Contact")
    contact_doc.update({
        "first_name": kyc_data["customer_name"],
        "mobile_no": primary_contact_number,
        "is_primary_contact": 1
    })
    has_primary_email = next(filter(lambda i: i.is_primary, contact_doc.email_ids), None)
    is_email_exists = next(filter(lambda i: i.email_id, contact_doc.email_ids), None)
    if is_email_exists:
        is_email_exists.is_primary = 1
    else:
        if has_primary_email:
            has_primary_email.is_primary = 0
        contact_doc.append("email_ids", {
            "email_id": kyc_data.email_id,
            "is_primary": 1,
        })
    contact_doc.append("links", {
        "link_doctype": "Customer",
        "link_name": kyc_doc.name,
    })
    has_primary_number = next(filter(lambda i: i.is_primary_mobile_no, contact_doc.phone_nos), None)
    is_number_exists = next(filter(lambda i: i.contact_number, contact_doc.phone_nos), None)
    if is_number_exists:
        is_number_exists.is_primary_mobile_no = 1
    else:
        if has_primary_number:
            has_primary_number.is_primary_mobile_no = 0
        contact_doc.append("phone_nos", {
            "contact_number": primary_contact_number,
            "is_primary_mobile_no": 1
        })
    if kyc_doc.unv_customer:
        contact_numbers = get_contact_numbers("Unverified Customer", kyc_doc.unv_customer)
        for contact_no in contact_numbers:
            contact_doc.append("phone_nos", {
            "contact_number": contact_no,
        })
    if kyc_doc.customer_primary_contact:
        contact_doc.save(ignore_permissions=True)
    else:
        contact_doc.insert(ignore_permissions=True)
    contact_name = contact_doc.name
    return contact_name

def create_address(kyc_doc, address_data, address_type):
    address_type_check = "is_primary_address" if address_type == "Billing" else "is_shipping_address"
    address_dict = {
        "address_title": address_data["title"],
        "address_type": address_type,
        address_type_check : 1,
        "address_line1": address_data["address_line1"],
        "address_line2": address_data["address_line2"],
        "district": address_data["city"],
        "city": address_data["city"],
        "state" : address_data["state"],
        "pincode": address_data["pincode"],
    }
    if address_data.get("address"):
        addr_doc = frappe.get_doc("Address", address_data.get("address"))
        addr_doc.update(address_dict)
        addr_doc.append("links",{
            "link_doctype": "Customer",
            "link_name": kyc_doc.name
        })
        addr_doc.save(ignore_permissions=True)
    else:
        addr_doc = frappe.new_doc("Address")
        addr_doc.update(address_dict)
        addr_doc.append("links",{
            "link_doctype": "Customer",
            "link_name": kyc_doc.name
        })
        addr_doc.insert(ignore_permissions=True)
    address_name = addr_doc.name
    return address_name

@frappe.whitelist()
def kyc_exists_validation(unv_customer):
    kyc_exists = frappe.db.exists("Customer", {"unv_customer": unv_customer, "kyc_status": ["in", ["Pending", "Completed"]]})
    if kyc_exists:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['kyc_exists'] = False
        frappe.local.response['message'] = f"KYC exists for the customer {unv_customer}"
    else:
        frappe.local.response['kyc_exists'] = True
        frappe.local.response['message'] = f"No KYC Created for the customer {unv_customer}"