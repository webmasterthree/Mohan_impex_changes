# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, add_days, date_diff

def execute(filters=None):
    columns = [
        {
            "label": "Batch No",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Batch",   # makes it clickable
            "width": 150,
        },
        {
            "label": "Item",
            "fieldname": "item",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "label": "Expiry Date",
            "fieldname": "expiry_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Remaining Days",
            "fieldname": "remaining_days",
            "fieldtype": "Int",
            "width": 120,
        },
    ]

    today = nowdate()
    threshold_date = add_days(today, 30)

    records = frappe.db.get_all(
        "Batch",
        fields=["name", "item", "expiry_date"],
        filters={"expiry_date": ["between", [today, threshold_date]]},
        order_by="expiry_date asc",
    )

    data = []
    for r in records:
        data.append({
            "name": r.name,  # this will now link to the Batch DocType
            "item": r.item,
            "expiry_date": r.expiry_date,
            "remaining_days": date_diff(r.expiry_date, today),
        })

    return columns, data
