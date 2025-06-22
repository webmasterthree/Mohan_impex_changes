import frappe
import json

@frappe.whitelist()
def get_reports_to_filter(role):
    reports_to_role = frappe.get_value("Roles and Reports To", {"employee_role": role}, "reports_to_role")
    return reports_to_role

@frappe.whitelist()
def set_user_permissions(self, status):
    frappe.db.set_value("User", {"name": self.user_id}, "role_profile_name", self.role_profile)
    if self.role_profile:
        if self.role_profile == "TSM":
            set_employee_permission(self)
        if self.role_profile == "SE":
            set_employee_permission(self, apply_to_all_doc=0, applicable_for="Trial Target")
        set_territory_permission(self)

def set_employee_permission(self, apply_to_all_doc=1, applicable_for=None):
    filters = {
        "for_value": self.name,
        "allow": "Employee", 
        "user": self.user_id,
        "apply_to_all_doctypes": apply_to_all_doc,
        "applicable_for": applicable_for 
    }
    emp_user_perm = frappe.get_value("User Permission", filters, ["name"])
    if not emp_user_perm:
        filters.update({"doctype": "User Permission"})
        doc = frappe.get_doc(filters)
        doc.insert(ignore_permissions=True)

def set_territory_permission(self):
    user  = self.user_id
    is_multiple_area = self.is_multiple_area_management
    area = self.area
    multiple_area = self.multiple_areas
    if is_multiple_area:
        multiple_area = json.loads(multiple_area)
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
        doc = frappe.get_doc({
            "doctype": "User Permission",
            "user": user,
            "allow": "Territory",
            "for_value": area
        })
        doc.save()
    for user_perm in user_perm_to_remove:
        frappe.delete_doc("User Permission", user_perm["name"])