import frappe
from frappe.utils import flt

from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote as ERPNextDeliveryNote


class CustomDeliveryNote(ERPNextDeliveryNote):
    def on_submit(self):
        super().on_submit()

        # Extra fallback because standard update_prevdoc_status is not updating SO delivered qty
        self.force_update_sales_order_delivered_qty()

    def on_cancel(self):
        super().on_cancel()

        # Recalculate SO delivered qty again after DN cancellation
        self.force_update_sales_order_delivered_qty()

    def force_update_sales_order_delivered_qty(self):
        sales_order_items = set()

        for row in self.items:
            if row.so_detail:
                sales_order_items.add(row.so_detail)

        sales_orders = set()

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