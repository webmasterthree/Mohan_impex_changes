# myapp/api/bin.py

import frappe
from frappe import whitelist

@whitelist()
def get_item_stock(item_code=None, warehouse=None):
    if not item_code or not warehouse:
        return {"error": "Missing item_code or warehouse"}

    result = frappe.db.get_value(
        "Bin",
        filters={"item_code": item_code, "warehouse": warehouse},
        fieldname="actual_qty"
    )

    return {
        "item_code": item_code,
        "warehouse": warehouse,
        "actual_qty": result or 0.0
    }
