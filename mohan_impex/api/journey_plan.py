import frappe
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm

@frappe.whitelist()
def journey_plan_list():
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
            tab_filter = 'workflow_state != "Approved"'
        else:
            tab_filter = 'workflow_state = "%s"'%(tab)
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area", "role_profile"], as_dict=True)
        role_filter = get_role_filter(emp, is_self, other_employee)
        is_self_filter = get_self_filter_status()
        order_by = " order by creation desc "
        query = """
            select name, created_date, IF(workflow_state='Approved', approved_date, IF(workflow_state='Rejected', rejected_date, created_date)) AS status_date, workflow_state as status, created_by_emp, created_by_name, COUNT(*) OVER() AS total_count
            from `tabJourney Plan`
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "date": "date",
            "status": "status",
            "nature_of_travel": "nature_of_travel",
            "mode_of_travel": "mode_of_travel"
        }
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key) and key == "date":
                and_filters.append(""" visit_from_date <= "{0}" AND visit_to_date >= "{0}" """.format(frappe.form_dict[key]))
            elif frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_by
        query += pagination
        journey_info = frappe.db.sql(query, as_dict=True)
        for journey in journey_info:
            journey["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.journey_plan.journey_form?name={journey['name']}"
        total_count = 0
        if journey_info:
            total_count = journey_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": journey_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter,
                "create": has_create_perm("Journey Plan")
            }
        ]
        # if frappe.has_permission("Journey Plan", "create"):
        #     response["create_perm"] = True
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Journey Plan list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def journey_plan_form():
    journey_name = frappe.form_dict.get("name")
    try:
        if journey_name:
            if not frappe.db.exists("Journey Plan", journey_name):
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['status'] = False
                frappe.local.response['message'] = "Please give valid Journey Plan ID"
                return
            journey_doc = frappe.get_doc("Journey Plan", journey_name)
            journey_doc = journey_doc.as_dict()
            activities = get_comments("Journey Plan", journey_doc["name"])
            journey_doc["activities"] = activities
            is_self_filter = get_self_filter_status()
            journey_doc["status_fields"] = get_workflow_statuses("Journey Plan", journey_name, get_session_emp_role())
            journey_doc["has_toggle_filter"] = is_self_filter
            journey_doc["created_person_mobile_no"] = frappe.get_value("Employee", journey_doc.get("created_by_emp"), "custom_personal_mobile_number")
            frappe.local.response['status'] = True
            frappe.local.response['message'] = "Journey Plan form has been successfully fetched"
            frappe.local.response['data'] = [journey_doc]
    except Exception as err:
        get_exception(err)
    
@frappe.whitelist()
def create_journey_plan():
    journey_plan_data = frappe.form_dict
    journey_plan_data.pop("cmd")
    journey_plan_data.update({
        "doctype" : "Journey Plan",
        "created_by_emp": get_session_employee(),
        "area": get_session_employee_area()
    })
    try:
        journey_plan_doc = frappe.get_doc(journey_plan_data)
        journey_plan_doc.save()
        response = {
            "journey_plan": journey_plan_doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Journey Plan has been successfully created"
        frappe.local.response['data'] = [response]
    except Exception as err:
        get_exception(err)
