import frappe
from frappe import _

@frappe.whitelist()
def get_item_supplier_lead_times(item_code):
    if not item_code:
        return {"error": "Missing item_code"}

    try:
        item = frappe.get_doc("Item", item_code)
        result = []
        for supplier in item.supplier_items:
            result.append({
                "item_code": item_code,
                "custom_lead_time_in_days": supplier.custom_lead_time_in_days
            })
        return result
    except frappe.DoesNotExistError:
        return {"error": f"Item {item_code} does not exist"}
    except Exception as e:
        return {"error": str(e)}
