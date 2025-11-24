import frappe

@frappe.whitelist(methods=["GET"])
def get_city_id(city=None):
    if not city:
        return ""

    # Try match by city field
    res = frappe.db.get_value("City", {"city": ["like", city]}, "name")

    # If not found, try match by name
    if not res:
        res = frappe.db.get_value("City", {"name": ["like", city]}, "name")

    return res or ""



@frappe.whitelist(methods=["GET"])
def get_district_id(district=None):
    if not district:
        return ""

    # Try match by district field
    res = frappe.db.get_value("District", {"district": ["like", district]}, "name")

    # If not found, try match by name field
    if not res:
        res = frappe.db.get_value("District", {"name": ["like", district]}, "name")

    return res or ""



@frappe.whitelist(methods=["GET"])
def get_state_id(state=None):
    if not state:
        return ""

    # Try match by state field
    res = frappe.db.get_value("State", {"state": ["like", state]}, "name")

    # If not found, try match by name field
    if not res:
        res = frappe.db.get_value("State", {"name": ["like", state]}, "name")

    return res or ""
