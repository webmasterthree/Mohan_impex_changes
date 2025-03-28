import frappe
from mohan_impex.mohan_impex.utils import get_session_employee
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter

@frappe.whitelist()
def journey_plan_list():
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
        order_by = " order by creation desc "
        query = """
            select name, approved_date, rejected_date, created_date, workflow_state as status, COUNT(*) OVER() AS total_count
            from `tabJourney Plan`
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "date": "date",
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
                "current_page": current_page
            }
        ]
        # if frappe.has_permission("Journey Plan", "create"):
        #     response["create_perm"] = True
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Journey Plan list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

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
            activities = [{
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
            },{
                "role": "ASM",
                "name": "Ravi",
                "status": "Approved",
                "comments": "Aproving the status",
                "date": "2025-02-14",
                "time": "13:58:32"
            }]
            activities = get_comments("Journey Plan", journey_doc["name"])
            journey_doc["activities"] = activities
            frappe.local.response['status'] = True
            frappe.local.response['message'] = "Journey Plan form has been successfully fetched"
            frappe.local.response['data'] = [journey_doc]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"
    
@frappe.whitelist()
def create_journey_plan():
    journey_plan_data = frappe.form_dict
    journey_plan_data.pop("cmd")
    journey_plan_data.update({
        "doctype" : "Journey Plan",
        "created_by_emp": get_session_employee()
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
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"
