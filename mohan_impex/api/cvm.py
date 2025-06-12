import frappe
import frappe.utils
from mohan_impex.mohan_impex.doctype.customer_visit_management.customer_visit_management import CustomerVisitManagement
from mohan_impex.mohan_impex.utils import get_session_employee_area
from mohan_impex.api import create_contact_number
from frappe.model.workflow import apply_workflow
import math
from mohan_impex.api import get_signed_token, get_role_filter, get_address_text
from mohan_impex.mohan_impex.comment import get_comments

@frappe.whitelist()
def cvm_list():
    try:
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
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp)
        query = """
            select cvm.name, shop_name, cl.contact, location, customer_level, kyc_status, workflow_state, COUNT(*) OVER() AS total_count
            from `tabCustomer Visit Management` as cvm
            JOIN `tabContact List` as cl on cl.parent = cvm.name
            where {tab_filter} and {role_filter}
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        order_and_group_by = " group by cvm.name order by cvm.creation desc "
        filter_checks = {
            "customer_type": "customer_type",
            "visit_type": "customer_level",
            "kyc_status": "kyc_status",
            "has_trial_plan": "has_trial_plan"
        }
        or_filters = []
        if frappe.form_dict.get("kyc_status"):
            frappe.form_dict["visit_type"] = "Primary"
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (shop_name LIKE "%{search_text}%" or cl.contact LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_and_group_by
        query += pagination
        cvm_info = frappe.db.sql(query, as_dict=True)
        for cvm in cvm_info:
            image_url = frappe.get_value("File", {"attached_to_name": cvm['name']}, "file_url")
            if image_url:
                image_url = get_signed_token(image_url)
            cvm["location"] = get_address_text(cvm["location"]) if cvm["location"] else ""
            cvm["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.cvm.cvm_form?name={cvm['name']}"
            cvm["image_url"] = image_url
            # cvm_list.append(cvm)
        total_count = 0
        if cvm_info:
            total_count = cvm_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": cvm_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Visit history list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def cvm_form():
    cvm_name = frappe.form_dict.get("name")
    try:
        if cvm_name:
            if not frappe.db.exists("Customer Visit Management", cvm_name):
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['status'] = False
                frappe.local.response['message'] = "Please give valid visit ID"
                return
            cvm_doc = frappe.get_doc("Customer Visit Management", cvm_name)
            image_url = frappe.get_all("File", {"attached_to_name": cvm_name}, ["name", "file_name", "file_url"])
            for image in image_url:
                image["url"] = get_signed_token(image["file_url"])
            cvm_doc = cvm_doc.as_dict()
            fields_to_remove = ["owner", "creation", "modified", "modified_by", "docstatus", "idx", "amended_from", "doctype", "parent", "parenttype", "parentfield", "area"]
            child_doc = ["product_pitching", "product_trial", "item_trial", "contact"]
            cvm_doc = {
                key: value for key, value in cvm_doc.items() if key not in fields_to_remove
            }
            for child_name in child_doc:
                if child_name in cvm_doc:
                    cvm_doc[child_name] = [
                        {k: v for k, v in item.items() if k not in fields_to_remove}
                        for item in cvm_doc[child_name]
                    ]
            grouped = {}
            for item in cvm_doc.get("product_pitching"):
                product = item["product"]
                if product in grouped:
                    grouped[product].append(item)
                else:
                    grouped[product] = [item]
            cvm_doc["product_pitching"] = [{"product": product, "items": items} for product, items in grouped.items()]
            trial_grouped = {}
            for item in cvm_doc.get("trial_table"):
                item["item_name"] = frappe.get_value("Item", {"name": item["item_code"]}, "item_name")
                product = item["product"]
                if product in trial_grouped:
                    trial_grouped[product].append(item)
                else:
                    trial_grouped[product] = [item]
            cvm_doc["trial_table"] = [{"product": product, "items": items} for product, items in trial_grouped.items()]
            activities = get_comments("Customer Visit Management", cvm_doc["name"])
            cvm_doc["activities"] = activities
            cvm_doc["image_url"] = image_url
            frappe.local.response['status'] = True
            frappe.local.response['message'] = "Visit form has been successfully fetched"
            frappe.local.response['data'] = [cvm_doc]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def create_cvm():
    cvm_data = frappe.form_dict
    cvm_data.pop("cmd")
    cvm_data.update({
        "area": get_session_employee_area()
    })
    try:
        response = {}
        if not cvm_validate(cvm_data):
            return
        if cvm_data.customer_type == "Existing":
            for contact in cvm_data.contact:
                if not frappe.db.exists("Contact Number", contact["contact"]):
                    create_contact_number(contact["contact"], "Customer", cvm_data.customer)
        if cvm_data.customer_type == "New":
            shop = create_shop(cvm_data.shop, cvm_data.shop_name)
            if shop: cvm_data.shop = shop
            created_contact = []
            for contact in cvm_data.contact:
                if not frappe.db.exists("Contact Number", contact["contact"]):
                    create_contact_number(contact["contact"])
                created_contact.append(contact["contact"])
            unv_cus_dict = {
                "doctype": "Unverified Customer",
                "customer_name": cvm_data.unv_customer_name,
                "customer_level": cvm_data.customer_level,
                "shop": cvm_data.shop,
                "shop_name": cvm_data.shop_name,
                "contact": cvm_data.contact,
                "address_line1": cvm_data.address_line1,
                "address_line2": cvm_data.address_line2,
                "district": cvm_data.district,
                "state": cvm_data.state,
                "pincode": cvm_data.pincode,
                "area": get_session_employee_area(),
            }
            if cvm_data.get("isupdate"):
                unv_cus = frappe.get_doc("Unverified Customer", cvm_data.get("unv_customer"))
                unv_cus.update(unv_cus_dict)
                unv_cus.save()
            else:
                unv_cus = frappe.new_doc('Unverified Customer')
                unv_cus.update(unv_cus_dict)
                unv_cus.insert(ignore_permissions=True, ignore_mandatory=True)
            address_dict = {
                "doctype":"Address",
                "address_type": "Billing",
                "address_title": cvm_data.unv_cus,
                "address_line1": cvm_data.address_line1,
                "address_line2": cvm_data.address_line2,
                "district": cvm_data.district,
                "city": cvm_data.district,
                "state": cvm_data.state,
                "pincode": cvm_data.pincode
            }
            if cvm_data.location and cvm_data.isupdate:
                addr_doc = frappe.get_doc("Address", cvm_data.location)
                addr_doc.update(address_dict)
                addr_doc.save(ignore_permissions=True)
            else:
                addr_doc = frappe.new_doc("Address")
                addr_doc.update(address_dict)
                addr_doc.append("links",{
                    "link_doctype": "Unverified Customer",
                    "link_name": unv_cus.name
                })
                addr_doc.insert(ignore_permissions=True)
            cvm_data.location = addr_doc.name
            unv_cus.address = cvm_data.location
            unv_cus.save()
            for contact in created_contact:
                create_contact_number(contact, "Unverified Customer", unv_cus.name)
            cvm_data.unv_customer = unv_cus.name
        doctype = "Customer Visit Management"
        if cvm_data.get("isupdate"):
            cvm_doc = frappe.get_doc(doctype, cvm_data.get("cvm_id"))
            cvm_doc.update(cvm_data)
            cvm_doc.save()
        else:
            cvm_data.update({"doctype": doctype})
            cvm_doc = frappe.get_doc(cvm_data)
            cvm_doc.insert()
        for image in cvm_data.captured_images:
            doc = frappe.get_doc("File", image.get("name"))
            doc.attached_to_doctype = doctype
            doc.attached_to_name = cvm_doc.name
            doc.save()
        cvm_doc.trial_plan()
        message = "Customer Visit request form has been successfully created as Draft"
        if cvm_data.action == "Submit":
            apply_workflow(cvm_doc, "Submit")
            message = "Customer Visit request form has been successfully submitted"
        response.update({
            "cvm": cvm_doc.name
        })
        frappe.local.response['status'] = True
        frappe.local.response['message'] = message
        frappe.local.response['data'] = [response]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

def create_shop(shop, shop_name):
    if not shop:
        doc = frappe.get_doc({
            "doctype": "Shop",
            "shop_name": shop_name
        })
        doc.insert(ignore_permissions=True)
        return doc


def cvm_validate(cvm_data):
    valid = True
    if cvm_data.customer_type == "New" and not cvm_data.unv_customer_name:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"Unverified Customer name is needed"
        return
    if cvm_data.customer_type == "Existing":
        if not cvm_data.location:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = f"Location is Missing"
            return
        if not frappe.db.exists("Address", cvm_data.location):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = f"Given location {cvm_data.location} not found in the system"
            return
        if cvm_data.customer_level == "Primary" and cvm_data.verific_type == "Unverified" and not cvm_data.unv_customer:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = f"Unverified Customer is Missing"
            return
        if cvm_data.customer_level == "Secondary" and cvm_data.verific_type == "Verified" and not cvm_data.customer:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = f"KYC Customer is Missing"
            return
    return valid

@frappe.whitelist()
def capture_image():
    if not frappe.request.files:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Image Files Not Found"
        return
    response = []
    try:
        for key in frappe.request.files:
            file = frappe.request.files[key]
            filename = file.filename
            file_doc = frappe.get_doc({
                    "doctype": "File",
                    "file_name": filename,
                    "content": file.read(),
                })
            file_doc.insert(ignore_permissions=True)  # Insert the file document
            frappe.db.commit()
            response.append({
                "name": file_doc.name,
                "file_name": file_doc.file_name,
                "file_url": file_doc.file_url,
                "url": frappe.utils.get_url() + file_doc.file_url
            })
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Captured Image has been saved"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def convert_to_order(cvm_id):
    try:
        if cvm_id:
            if not frappe.db.exists("Customer Visit Management", cvm_id):
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['status'] = False
                frappe.local.response['message'] = "Please give valid visit ID"
                return
            doc = CustomerVisitManagement("Customer Visit Management", cvm_id)
            response = doc.create_order(return_so_id=True)
            frappe.local.response['status'] = True
            frappe.local.response['message'] = f"Sales Order has been created for the visit {cvm_id}"
            frappe.local.response['data'] = [response]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def get_customer_address():
    try:
        if not frappe.form_dict.get("customer"):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = f"Give customer value for filter"
            return
        if not frappe.form_dict.get("verific_type"):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = f"Give verification type for filter"
            return
        customer = frappe.form_dict.get("customer")
        if frappe.form_dict.get("verific_type") == "Verified":
            address_name = frappe.get_value("Customer", {"name": customer}, "customer_primary_address")
        else:
            address_name = frappe.get_value("Unverified Customer", {"name": customer}, "address")
        address_dict = {}
        if address_name:
            address_doc = frappe.get_doc("Address", address_name)
            address_dict = {
                "name": address_doc.name,
                "address_title": address_doc.address_title,
                "address_line1": address_doc.address_line1,
                "address_line2": address_doc.address_line2,
                "district": address_doc.district,
                "state": address_doc.state,
                "pincode": address_doc.pincode
            }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Address has been fetched"
        frappe.local.response['data'] = address_dict
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"
