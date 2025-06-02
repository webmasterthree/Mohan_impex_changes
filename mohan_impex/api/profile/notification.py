import frappe
from mohan_impex.api import get_signed_token
import math
from bs4 import BeautifulSoup
import html

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
        filters = {
            "for_user": frappe.session.user
        }
        filters["read"] = "0" if frappe.form_dict.get("unread") == "1" else "1"
        notific_info = frappe.get_list(
            "Notification Log",
            fields=[
                "name", "subject", "email_content as content", "from_user", "creation", "COUNT(*) OVER() AS total_count"
            ],
            filters=filters,
            order_by="creation desc",
            limit=limit,
            start=offset
        )
        default_user_image = frappe.get_single("Mohan Impex Settings").default_profile_image
        default_user_image = get_signed_token(default_user_image)
        for notific in notific_info:
            notific["subject"] = BeautifulSoup(notific["subject"], "html.parser").get_text(separator=" ").strip() if notific["subject"] else ""
            notific["subject"] = ' '.join(notific["subject"].split())
            notific["content"] = BeautifulSoup(notific["content"], "html.parser").get_text(separator=" ").strip() if notific["content"] else ""
            notific["creation"] = frappe.utils.time_diff_in_seconds(frappe.utils.now(), notific["creation"])
            notific["creation"] = frappe.utils.format_duration(notific["creation"], False)
            notific["creation"] = notific["creation"].split(" ")[0]
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

@frappe.whitelist()
def mark_as_read():
    try:
        frappe.db.set_value("Notification Log", {"for_user": frappe.session.user, "read": 0}, "read", 1)
        frappe.db.commit()
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Notifications has been marked as read"
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"
