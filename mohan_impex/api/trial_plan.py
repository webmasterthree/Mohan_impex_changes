import frappe
from mohan_impex.api.cvm import create_contact_number 
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm

@frappe.whitelist()
def trial_list():
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
        if tab == "Pending":
            tab_filter = 'workflow_state in ("%s", "%s")'%("Pending", "Rejected")
        else:
            tab_filter = 'workflow_state = "%s"'%(tab)
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area", "role_profile"], as_dict=True)
        role_filter = get_role_filter(emp, is_self, other_employee)
        is_self_filter = get_self_filter_status()
        order_and_group_by = " group by pt.name order by pt.creation desc "
        query = """
            select pt.name, created_date, IF(workflow_state='Approved', approved_date, IF(workflow_state='Rejected', rejected_date, created_date)) AS status_date, shop_name, cl.contact, location, workflow_state, created_by_emp, created_by_name, COUNT(*) OVER() AS total_count
            from `tabTrial Plan` as pt
            Join `tabContact List` as cl on cl.parent = pt.name
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "conduct_by": "conduct_by",
            "trial_loc": "trial_loc",
            "customer_level": "customer_level",
            "status": "status"
        }
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (pt.name LIKE "%{search_text}%" or pt.customer_name LIKE "%{search_text}%" or cl.contact LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
            and_filters.append("""pt.date between "{0}" and "{1}" """.format(frappe.form_dict["from_date"], frappe.form_dict["to_date"]))
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_and_group_by
        query += pagination
        trial_info = frappe.db.sql(query, as_dict=True)
        total_count = 0
        if trial_info:
            total_count = trial_info[0]["total_count"]
        page_count = math.ceil(total_count / limit)
        response = [
            {
                "records": trial_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter,
                "create": has_create_perm("Trial Plan")
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial plan list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def trial_form():
    try:
        trial_name = frappe.form_dict.get("name")
        if not trial_name:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give Trial Name"
            return
        if not frappe.db.exists("Trial Plan", trial_name):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give valid trial plan ID"
            return
        trial_doc = frappe.get_doc("Trial Plan", trial_name)
        trial_doc = trial_doc.as_dict()
        fields_to_remove = ["owner", "creation", "modified", "modified_by", "docstatus", "idx", "amended_from", "parent", "parenttype", "parentfield", "area"]
        child_doc = ["trial_item_table", "product_trial_table", "item_trial_table"]
        trial_doc = {
            key: value for key, value in trial_doc.items() if key not in fields_to_remove
        }
        for child_name in child_doc:
            if child_name in trial_doc:
                trial_doc[child_name] = [
                    {k: v for k, v in item.items() if k not in fields_to_remove}
                    for item in trial_doc[child_name]
                ]
        grouped = {}
        for item in trial_doc.get("trial_plan_table"):
            product = item["product"]
            if product in grouped:
                grouped[product].append(item)
            else:
                grouped[product] = [item]
        trial_doc["trial_plan_table"] = [{"product": product, "items": items} for product, items in grouped.items()]
        activities = get_comments("Trial Plan", trial_doc["name"])
        trial_doc["activities"] = activities
        trial_doc["tsm_info"] = frappe.get_value("Employee", {"name": trial_doc["assigned_to_emp"]}, ["employee_name as name", "cell_number as mobile", "company_email as email"], as_dict=True) or {}
        is_self_filter = get_self_filter_status()
        trial_doc["status_fields"] = get_workflow_statuses("Trial Plan", trial_name, get_session_emp_role())
        trial_doc["has_toggle_filter"] = is_self_filter
        trial_doc["created_person_mobile_no"] = frappe.get_value("Employee", trial_doc.get("created_by_emp"), "custom_personal_mobile_number")
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial Plan form has been successfully fetched"
        frappe.local.response['data'] = [trial_doc]
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def create_product_trial():
    trial_data = frappe.form_dict
    trial_data.pop("cmd")
    trial_data.update({
        "doctype" : "Trial Plan",
        "created_by_emp": get_session_employee(),
        "area": get_session_employee_area()
    })
    try:
        if not trial_validate(trial_data):
            return
        if trial_data.verific_type == "Verified":
            cont_doctype = "Customer"
            cont_link_name = trial_data.customer
        else:
            cont_doctype = "Unverified Customer"
            cont_link_name = trial_data.unv_customer
        for contact in trial_data.contact:
            if not frappe.db.exists("Contact Number", contact["contact"]):
                create_contact_number(contact["contact"], cont_doctype, cont_link_name)
        trial_doc = frappe.get_doc(trial_data)
        trial_doc.save()
        response = {
            "trial": trial_doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial plan has been successfully submitted"
        frappe.local.response['data'] = [response]
    except Exception as err:
        get_exception(err)

def trial_validate(trial_data):
    valid = True
    if not trial_data.location:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Location is Missing"
        return
    if not frappe.db.exists("Address", trial_data.location):
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"Given location {trial_data.location} not found in the system"
        return
    if trial_data.customer_level == "Primary" and trial_data.verific_type == "Unverified" and not trial_data.unv_customer:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"Unverified Customer is Missing"
        return
    if trial_data.verific_type == "Verified" and not trial_data.customer:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"KYC Customer is Missing"
        return
    return valid

@frappe.whitelist()
def update_trial_timing():
    try:
        trial_id = frappe.form_dict.get("trial_id")
        trial_start = frappe.form_dict.get("trial_start")
        trial_end = frappe.form_dict.get("trial_end")
        
        if not trial_id:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Trial ID is missing"
            return
        
        if not frappe.db.exists("Trial Plan", trial_id):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Invalid trial plan ID"
            return

        if not trial_start and not trial_end:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Trial start or end time is missing"
            return

        trial_doc = frappe.get_doc("Trial Plan", trial_id)
        trial_doc.trial_start = trial_start
        trial_doc.trial_end = trial_end
        trial_doc.save()
        
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial timing have been successfully updated"
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or str(err)

@frappe.whitelist()
def assign_to_employee(trial_id, assigned_to_emp):
    try:
        trial_doc = frappe.get_doc("Trial Plan", trial_id)
        trial_doc.assigned_to_emp = assigned_to_emp
        trial_doc.save()
        emp_name = frappe.get_value("Employee", assigned_to_emp, "employee_name")
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial plan {0} has been successfully assigned to {1}".format(trial_id, emp_name)
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or str(err)