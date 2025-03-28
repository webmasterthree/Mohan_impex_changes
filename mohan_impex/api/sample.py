import frappe
from mohan_impex.mohan_impex.utils import get_session_employee
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter

@frappe.whitelist()
def sample_list():
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
            tab_filter = 'workflow_state in ("%s", "%s")'%("Approved", "Received")
        if frappe.form_dict.get("show_area_records"):
            show_area_records = int(frappe.form_dict.get("show_area_records"))
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp, show_area_records)
        order_by = " order by creation desc "
        query = """
            select name, approved_date, workflow_state as status, COUNT(*) OVER() AS total_count
            from `tabSample Requisition`
            where {tab_filter} and {role_filter}
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        filter_checks = {
            "status": "status",
            "reqd_date": "reqd_date"
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
        sample_info = frappe.db.sql(query, as_dict=True)
        for sample in sample_info:
            sample["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.sample.sample_form?name={sample['name']}"
        # if frappe.has_permission("Sample Requisition", "create"):
        #     response["create_perm"] = True
        total_count = 0
        if sample_info:
            total_count = sample_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": sample_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sample Request list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def sample_form():
    sample_name = frappe.form_dict.get("name")
    try:
        if not sample_name:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give Sample Request ID"
            return
        if not frappe.db.exists("Sample Requisition", sample_name):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give valid Sample Request ID"
            return
        sample_doc = frappe.get_doc("Sample Requisition", sample_name)
        sample_doc = sample_doc.as_dict()
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
        activities = get_comments("Sample Requisition", sample_doc["name"])
        sample_doc["activities"] = activities
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sample request form has been successfully fetched"
        frappe.local.response['data'] = [sample_doc]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def create_sample():
    sample_data = frappe.form_dict
    sample_data.pop("cmd")
    sample_data.update({
        "doctype" : "Sample Requisition",
        "created_by_emp": get_session_employee()
    })
    try:
        sample_doc = frappe.get_doc(sample_data)
        sample_doc.save()
        response = {
            "sample": sample_doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sample request form has been successfully created"
        frappe.local.response['data'] = [response]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"