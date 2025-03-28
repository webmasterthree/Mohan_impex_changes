import frappe
from mohan_impex.api.cvm import create_contact_number 
from mohan_impex.mohan_impex.utils import get_session_employee
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter

@frappe.whitelist()
def trial_list():
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
        if tab == "Pending":
            tab_filter = 'workflow_state in ("%s", "%s")'%("Pending", "Rejected")
        else:
            tab_filter = 'workflow_state = "%s"'%(tab)
        if frappe.form_dict.get("show_area_records"):
            show_area_records = int(frappe.form_dict.get("show_area_records"))
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp, show_area_records)
        order_and_group_by = " group by pt.name order by pt.creation desc "
        query = """
            select pt.name, trial_type, approved_date, rejected_date, shop_name, cl.contact, location, created_by_emp, workflow_state, COUNT(*) OVER() AS total_count
            from `tabTrial Plan` as pt
            Join `tabContact List` as cl on cl.parent = pt.name
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "conduct_by": "conduct_by",
            "trial_loc": "trial_loc",
            "customer_level": "customer_level",
            "trial_type": "trial_type" 
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
                "current_page": current_page
            }
        ]
        # trial_list = []
        # for trial in trial_info:
        #     trial["location"] = trial["location"].rsplit('-', 1)[0] if trial["location"] else ""
        #     trial["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.trial_plan.trial_form?name={trial['name']}"
        #     trial_list.append(trial)
        # approved = list(filter(lambda d: d.get("workflow_state") == "Approved", trial_list))
        # pending = list(filter(lambda d: d.get("workflow_state") == "Pending", trial_list))

        # if frappe.has_permission("Trial Plan", "create"):
        #     response["create_perm"] = True
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial plan list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

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
        fields_to_remove = ["owner", "creation", "modified", "modified_by", "docstatus", "idx", "amended_from", "doctype", "parent", "parenttype", "parentfield", "created_by_emp", "area"]
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
        activities = [
                {
                    "role": "ASM",
                    "name": "Ravi",
                    "status": "Approved",
                    "comments": None,
                    "date": "2025-02-13",
                    "time": "13:58:32"
                },
                {
                    "role": "ASM",
                    "name": "Ravi",
                    "status": None,
                    "comments": "Aproving the status",
                    "date": "2025-02-14",
                    "time": "13:58:32"
                },
                {
                    "role": "ASM",
                    "name": "Ravi",
                    "status": "Approved",
                    "comments": "Aproving the status",
                    "date": "2025-02-14",
                    "time": "13:58:32"
                }
            ]
        activities = get_comments("Trial Plan", trial_doc["name"])
        trial_doc["activities"] = activities
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial Plan form has been successfully fetched"
        frappe.local.response['data'] = [trial_doc]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def create_product_trial():
    trial_data = frappe.form_dict
    trial_data.pop("cmd")
    trial_data.update({
        "doctype" : "Trial Plan",
        "created_by_emp": get_session_employee()
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
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

def trial_validate(trial_data):
    valid = True
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