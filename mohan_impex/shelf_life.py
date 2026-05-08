import frappe
from frappe.utils import date_diff, nowdate


@frappe.whitelist()
def remaining_shelf_life(batch):
    if not batch:
        frappe.throw("Please pass Batch")

    batch_doc = frappe.db.get_value(
        "Batch",
        batch,
        ["item", "manufacturing_date"],
        as_dict=True
    )

    if not batch_doc:
        frappe.throw(f"Batch {batch} not found")

    if not batch_doc.manufacturing_date:
        frappe.throw(f"Manufacturing Date is missing in Batch {batch}")

    shelf_life_days = frappe.db.get_value(
        "Item",
        batch_doc.item,
        "shelf_life_in_days"
    ) or 0

    days_since_mfg = date_diff(nowdate(), batch_doc.manufacturing_date)

    remaining_shelf_life_days = max(0, shelf_life_days - days_since_mfg)

    return remaining_shelf_life_days