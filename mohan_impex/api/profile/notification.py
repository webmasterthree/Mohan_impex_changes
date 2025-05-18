import frappe
from mohan_impex.api import get_signed_token
import math

@frappe.whitelist()
def notification_list():
    try:
        limit = frappe.form_dict.get("limit")
        current_page = frappe.form_dict.get("current_page")
        if not limit or not current_page:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Either limit or current page is missing"
            return
        current_page = int(current_page)
        limit = int(limit)
        offset = limit * (current_page - 1)
        pagination = "limit %s offset %s"%(limit, offset)
        query = """
            select name, subject, email_content, from_user, COUNT(*) OVER() AS total_count
            from `tabNotification Log` as nl
            where for_user = "{user_id}"
        """.format(user_id=frappe.session.user)
        order_and_group_by = " order by creation desc "
        and_filters = ""
        if frappe.form_dict.get("unread") == True:
            and_filters += """ and read = 0 """
        query += order_and_group_by
        query += pagination
        notific_info = frappe.db.sql(query, as_dict=True)
        default_user_image = frappe.get_single("Mohan Impex Settings").default_profile_image
        default_user_image = get_signed_token(default_user_image)
        for notific in notific_info:
            user_image = frappe.get_value("User", {"name": notific["from_user"]}, "user_image")
            notific["user_image"] = default_user_image
            if user_image: 
                notific["user_image"] = get_signed_token(notific["from_user"])
        total_count = 0
        if notific_info:
            total_count = notific_info[0]["total_count"]
        page_count = math.ceil(total_count / int(limit))
        response = [
            {
                "records": notific_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page
            }
        ]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Notification list has been successfully fetched"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"
