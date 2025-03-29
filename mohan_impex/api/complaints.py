import frappe
from mohan_impex.mohan_impex.utils import get_session_employee
from frappe.utils.file_manager import save_file
from mohan_impex.api import get_role_filter
import math
from mohan_impex.mohan_impex.comment import get_comments

@frappe.whitelist()
def complaints_list():
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
        if frappe.form_dict.get("show_area_records"):
            show_area_records = int(frappe.form_dict.get("show_area_records"))
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp, show_area_records)
        query = """
            select name, IF(workflow_state='Active', opening_date, IF(workflow_state='Resolved', resolved_date, opening_date)) AS status_date, customer_name, claim_type, workflow_state, created_by_emp, COUNT(*) OVER() AS total_count
            from `tabIssue`
            where {tab_filter} and {role_filter}
        """.format(tab_filter=tab_filter, role_filter=role_filter)
        order_and_group_by = " group by name order by creation desc "
        filter_checks = {
            "customer_level": "customer_level",
            "claim_type": "claim_type"
        }
        or_filters = []
        if frappe.form_dict.get("search_text"):
            or_filters = """AND (name LIKE "%{search_text}%" or invoice_no LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                and_filters.append("""{0} = "{1}" """.format(value, frappe.form_dict[key]))
        if frappe.form_dict.get("from_date") and frappe.form_dict.get("to_date"):
            and_filters.append(""" opening_date between "{0}" and "{1}" """.format(frappe.form_dict["from_date"], frappe.form_dict["to_date"]))
        and_filters = " AND ".join(and_filters)
        query += """ AND ({0})""".format(and_filters) if and_filters else ""
        query += order_and_group_by
        query += pagination
        complaints_info = frappe.db.sql(query, as_dict=True)
        for complaints in complaints_info:
            # complaints["workflow_state"] = "Pending" if complaints["workflow_state"] == "Open" else complaints["workflow_state"]
            # complaints["username"] = frappe.get_value("Employee", {"name": complaints["created_by_emp"]}, "employee_name")
            complaints["form_url"] = f"{frappe.utils.get_url()}/api/method/mohan_impex.api.complaints.complaints_form?name={complaints['name']}"
            complaints.pop("created_by_emp", None)
            # complaints_list.append(complaints)
        total_count = 0
        if complaints_info:
            total_count = complaints_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": complaints_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Complaints & Claims request list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def complaints_form():
    complaints_name = frappe.form_dict.get("name")
    try:
        if complaints_name:
            if not frappe.db.exists("Issue", complaints_name):
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['status'] = False
                frappe.local.response['message'] = "Please give valid Complaint ID"
                return
            complaints_doc = frappe.get_doc("Issue", complaints_name)
            complaints_dict = {
                "subject":  complaints_doc.subject,
                "claim_type":  complaints_doc.claim_type,
                "customer_level": complaints_doc.customer_level,
                "customer": complaints_doc.customer,
                "customer_name": complaints_doc.customer_name,
                "contact": complaints_doc.contact_number,
                "date": complaints_doc.opening_date,
                "shop": complaints_doc.shop,
                "shop_name": complaints_doc.shop_name,
                "invoice_no": complaints_doc.invoice_no,
                "invoice_date": complaints_doc.invoice_date,
                "district": complaints_doc.district,
                "state": complaints_doc.state,
                "pincode": complaints_doc.pincode,
                "description": complaints_doc.description,
            }
            complaint_item = []
            for item in complaints_doc.complaint_item:
                complaint_item.append({
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "complaint_itm_qty": item.complaint_itm_qty,
                    "value_of_goods": item.value_of_goods,
                    "batch_no": item.batch_no,
                    "expiry": item.expiry,
                    "mfd": item.mfd,
                })
            complaints_dict["complaint_item"] = complaint_item
            image_url = frappe.get_all("File", {"attached_to_name": complaints_name}, ["file_name","file_url"])
            site_url = frappe.utils.get_url()
            for url in image_url:
                url["file_url"] = f"{site_url}{url['file_url']}"
            complaints_dict["image_url"] = image_url
            activities = get_comments("Issue", complaints_name)
            complaints_dict["activities"] = activities
            frappe.local.response['status'] = True
            frappe.local.response['message'] = "Complaints & Claims request form has been successfully fetched"
            frappe.local.response['data'] = [complaints_dict]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def create_complaint():
    complaint_data = frappe.form_dict
    complaint_data.pop("cmd")
    complaint_data.update({
        "doctype" : "Issue",
        "created_by_emp": get_session_employee()
    })
    try:
        complaint_doc = frappe.new_doc("Issue")
        complaint_doc.update(complaint_data)
        complaint_doc.insert()
        for image in complaint_data.ref_attachments:
            doc = frappe.get_doc("File", image.get("name"))
            doc.attached_to_doctype = "Issue"
            doc.attached_to_name = complaint_doc.name
            doc.save()
        response = {
            "complaint": complaint_doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Complaints & Claims request form has been successfully created"
        frappe.local.response['data'] = [response]
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def complaint_attachments(complaint_id):
    frappe.local.response['data'] = []
    if not frappe.db.exists("Issue", complaint_id):
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Please give valid complaint ID"
        return
    if not frappe.request.files:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "File Input Not Found"
        return
    try:
        response = []
        for key in frappe.request.files:
            file = frappe.request.files[key]
            filename = file.filename
            doctype = "Issue"
            file_doc = save_file(filename, file.read(), doctype, complaint_id)
            response.append({
                "file_name": file_doc.file_name,
                "file_url": file_doc.file_url
            })
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Captured Image has been saved for the visit {complaint_id}"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"