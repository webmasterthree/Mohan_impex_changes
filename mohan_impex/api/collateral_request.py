import frappe
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm

@frappe.whitelist()
def collateral_request_list():
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
        order_by = " order by creation desc "
        query = """
            select name, created_date, IF(workflow_state='Approved', approved_date, IF(workflow_state='Rejected', rejected_date, created_date)) AS status_date, workflow_state as status, created_by_emp, created_by_name, COUNT(*) OVER() AS total_count
            from `tabMarketing Collateral Request`
            where {tab_filter} and {role_filter} 
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "created_date": "created_date",
            "status": "status"
        }
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_by
        query += pagination
        cr_info = frappe.db.sql(query, as_dict=True)
        cr_list = []
        for cr in cr_info:
            cr["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.collateral_request.collateral_request_form?name={cr['name']}"
            cr_list.append(cr)
        # if frappe.has_permission("Marketing Collateral Request", "create"):
        #     response["create_perm"] = True
        total_count = 0
        if cr_info:
            total_count = cr_info[0]["total_count"]
        page_count = math.ceil(total_count / limit)
        response = [
            {
                "records": cr_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter,
                "create": has_create_perm("Customer Visit Management")
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Collateral Request list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def collateral_request_form():
    cr_name = frappe.form_dict.get("name")
    try:
        if cr_name:
            if not frappe.db.exists("Marketing Collateral Request", cr_name):
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['status'] = False
                frappe.local.response['message'] = "Please give valid Marketing Collateral Request ID"
                return
            cr_doc = frappe.get_doc("Marketing Collateral Request", cr_name)
            cr_doc = cr_doc.as_dict()
            activities = get_comments("Marketing Collateral Request", cr_doc["name"])
            cr_doc["activities"] = activities
            is_self_filter = get_self_filter_status()
            cr_doc["status_fields"] = get_workflow_statuses("Marketing Collateral Request", cr_name, get_session_emp_role())
            cr_doc["has_toggle_filter"] = is_self_filter
            cr_doc["created_person_mobile_no"] = frappe.get_value("Employee", cr_doc.get("created_by_emp"), "custom_personal_mobile_number")
            frappe.local.response['status'] = True
            frappe.local.response['message'] = "Marketing Collateral Request form has been successfully fetched"
            frappe.local.response['data'] = [cr_doc]
    except Exception as err:
        get_exception(err)
    
@frappe.whitelist()
def create_collateral_request():
    cr_data = frappe.form_dict
    cr_data.pop("cmd")
    cr_data.update({
        "doctype" : "Marketing Collateral Request",
        "created_by_emp": get_session_employee(),
        "area": get_session_employee_area()
    })
    try:
        cr_doc = frappe.get_doc(cr_data)
        cr_doc.save()
        response = [{
            "cr_id": cr_doc.name
        }]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Collateral request has been successfully created"
        frappe.local.response['data'] = response
    except Exception as err:
        get_exception(err)
