import frappe
from mohan_impex.api import get_signed_token, get_exception

@frappe.whitelist()
def get_account_info():
    try:
        account_info = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["employee_name", "user_id as email_id", "custom_personal_mobile_number as mobile_number", "designation as position"], as_dict=1)
        if account_info.get("mobile_number") is None: account_info["mobile_number"] = ""
        user_image = frappe.get_value("User", {"name": frappe.session.user}, "user_image")
        default_user_image = frappe.get_single("Mohan Impex Settings").default_profile_image
        if not user_image: user_image = get_signed_token(default_user_image)
        else: user_image = get_signed_token(user_image)
        account_info["user_image"] = user_image
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Account Information list has been successfully fetched"
        frappe.local.response['data'] = account_info
    except Exception as err:
        get_exception(err)

@frappe.whitelist()
def update_account_info():
    try:
        account_info = frappe.form_dict
        account_info_dict = {
            "first_name": account_info.get("employee_name"),
            "last_name": "",
            "middle_name": "",
            "employee_name": account_info.get("employee_name"),
            "custom_personal_mobile_number": account_info.get("mobile_number")
        }
        frappe.db.set_value("Employee", {"user_id": frappe.session.user}, account_info_dict)
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Account Information has been successfully updated"
    except Exception as err:
        get_exception(err)
        
@frappe.whitelist()
def get_leader_board():
    try:
        leader_board = frappe.get_all("Leader Board", {"status": "Published"}, ["leader_board_name", "leader_board_content"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Leader Board list has been successfully fetched"
        frappe.local.response['data'] = leader_board
    except Exception as err:
        get_exception(err)