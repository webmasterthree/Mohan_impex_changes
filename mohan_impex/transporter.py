import frappe
from collections import defaultdict

@frappe.whitelist()
def get_supplier_driver_map():
    """Returns a mapping of transporter → list of driver dicts (with name and full_name)."""
    drivers = frappe.db.get_all('Driver', fields=["name", "full_name", "transporter"])

    supplier_driver_map = defaultdict(list)
    for driver in drivers:
        if driver['transporter']:
            supplier_driver_map[driver['transporter']].append({
                "name": driver["name"],
                "full_name": driver["full_name"]
            })

    return dict(supplier_driver_map)
