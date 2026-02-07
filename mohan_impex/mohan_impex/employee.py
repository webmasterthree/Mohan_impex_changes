import frappe
import json
from frappe.permissions import (
	add_user_permission,
	remove_user_permission,
)
@frappe.whitelist()
def get_reports_to_filter(role):
    reports_to_role = frappe.get_value("Roles and Reports To", {"employee_role": role}, "reports_to_role")
    return reports_to_role

@frappe.whitelist()
def set_user_permissions(self, status):
    if not self.is_new():
        frappe.db.set_value("User", {"name": self.user_id}, "role_profile_name", self.role_profile)
        user_permissions = frappe.get_all("User Permission", {"user": self.user_id}, ["allow", "for_value"])
        for permission in user_permissions:
            remove_user_permission(permission["allow"], permission["for_value"], self.user_id)
        if self.role_profile:
            if self.role_profile == "TSM":
                add_user_permission("Employee", self.name, self.user_id, True)
            if self.role_profile == "SE":
                add_user_permission(
                    doctype="Employee", 
                    name=self.name, 
                    user=self.user_id, 
                    ignore_permissions=True,
                    applicable_for="Trial Target"
                )
            if self.role_profile != "TSM":
                set_territory_permission(self)

def set_territory_permission(self):
    user  = self.user_id
    is_multiple_area = self.is_multiple_area_management
    area = self.area
    multiple_area = self.multiple_areas
    if is_multiple_area:
        areas = [area.get("area") for area in multiple_area]
    else:
        areas = [area]
    user_perm_with_area_list = frappe.get_all("User Permission", {"for_value": ["in", areas], "allow": "Territory", "user": user}, ["name", "for_value as area"])
    user_perm_list = frappe.get_all("User Permission", {"allow": "Territory", "user": user}, ["name", "for_value as area"])    
    area_set = set(areas)
    user_perm_with_area = {user_perm["area"] for user_perm in user_perm_with_area_list}
    user_perm = {user_perm["area"] for user_perm in user_perm_list}
    areas_to_create = list(area_set.difference(user_perm))
    area_to_remove = list(user_perm.difference(user_perm_with_area))
    user_perm_to_remove = list(filter(lambda user_perm: user_perm["area"] in area_to_remove, user_perm_list))
    for area in areas_to_create:
        add_user_permission("Territory", area, user, True)
    for user_perm in user_perm_to_remove:
        frappe.delete_doc("User Permission", user_perm["name"])