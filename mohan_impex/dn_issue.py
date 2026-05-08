import frappe
from frappe.utils import flt


@frappe.whitelist()
def update_sales_orders_from_delivery_notes(delivery_notes):
    """
    delivery_notes can be:
    1. Python list:
       ["DO-DNK-0662-26-27", "DO-DNK-0663-26-27"]

    2. JSON string:
       '["DO-DNK-0662-26-27", "DO-DNK-0663-26-27"]'

    3. Comma-separated string:
       "DO-DNK-0662-26-27,DO-DNK-0663-26-27"
    """

    if not delivery_notes:
        frappe.throw("Please provide Delivery Note list")

    if isinstance(delivery_notes, str):
        try:
            delivery_notes = frappe.parse_json(delivery_notes)
        except Exception:
            delivery_notes = [d.strip() for d in delivery_notes.split(",") if d.strip()]

    if not isinstance(delivery_notes, list):
        frappe.throw("Delivery Notes must be a list")

    sales_order_items = set()
    sales_orders = set()
    skipped = []

    for dn_name in delivery_notes:
        if not frappe.db.exists("Delivery Note", dn_name):
            skipped.append({
                "delivery_note": dn_name,
                "reason": "Delivery Note not found"
            })
            continue

        dn = frappe.get_doc("Delivery Note", dn_name)

        if dn.docstatus != 1:
            skipped.append({
                "delivery_note": dn_name,
                "reason": "Delivery Note is not submitted"
            })
            continue

        for row in dn.items:
            if row.so_detail:
                sales_order_items.add(row.so_detail)

            if row.against_sales_order:
                sales_orders.add(row.against_sales_order)

    for so_detail in sales_order_items:
        delivered_qty = frappe.db.sql("""
            select ifnull(sum(dni.qty), 0)
            from `tabDelivery Note Item` dni
            join `tabDelivery Note` dn on dn.name = dni.parent
            where dni.so_detail = %s
            and dni.docstatus = 1
            and dn.docstatus = 1
            and ifnull(dn.is_return, 0) = 0
        """, so_detail)[0][0]

        frappe.db.set_value(
            "Sales Order Item",
            so_detail,
            "delivered_qty",
            delivered_qty,
            update_modified=False
        )

        so_name = frappe.db.get_value("Sales Order Item", so_detail, "parent")
        if so_name:
            sales_orders.add(so_name)

    updated_sales_orders = []

    for so_name in sales_orders:
        so = frappe.get_doc("Sales Order", so_name)

        total_qty = sum(flt(row.qty) for row in so.items)
        total_delivered_qty = sum(flt(row.delivered_qty) for row in so.items)

        per_delivered = (total_delivered_qty / total_qty) * 100 if total_qty else 0

        if per_delivered >= 100:
            delivery_status = "Fully Delivered"
        elif per_delivered > 0:
            delivery_status = "Partly Delivered"
        else:
            delivery_status = "Not Delivered"

        frappe.db.set_value(
            "Sales Order",
            so_name,
            {
                "per_delivered": per_delivered,
                "delivery_status": delivery_status
            },
            update_modified=False
        )

        so.reload()
        so.set_status(update=True)
        so.db_update()

        updated_sales_orders.append({
            "sales_order": so_name,
            "per_delivered": per_delivered,
            "delivery_status": delivery_status
        })

    frappe.db.commit()

    return {
        "status": True,
        "message": "Sales Orders updated successfully",
        "delivery_notes_received": delivery_notes,
        "sales_order_items_updated": list(sales_order_items),
        "updated_sales_orders": updated_sales_orders,
        "skipped": skipped
    }