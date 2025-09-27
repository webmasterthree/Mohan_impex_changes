# mohan_impex/api/batch.py
import frappe
from frappe.utils import nowdate, add_days, date_diff

@frappe.whitelist(methods=["GET"])
def batches_expiring_soon():
    """
    REST API: Return batches expiring within 30 days.
    URL: /api/method/mohan_impex.api.batch.batches_expiring_soon
    """
    today = nowdate()
    threshold_date = add_days(today, 30)

    records = frappe.db.get_all(
        "Batch",
        fields=["name", "item", "expiry_date"],
        filters={"expiry_date": ["between", [today, threshold_date]]},
        order_by="expiry_date asc",
    )

    # add remaining_days
    for r in records:
        r["remaining_days"] = date_diff(r["expiry_date"], today)

    return {
        "today": today,
        "days": 30,
        "count": len(records),
        "data": records,
    }
