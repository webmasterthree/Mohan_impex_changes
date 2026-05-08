import frappe

from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt as ERPNextPurchaseReceipt


class CustomPurchaseReceipt(ERPNextPurchaseReceipt):
    def on_submit(self):
        super().on_submit()
        self.force_update_purchase_order_received_qty()

    def on_cancel(self):
        super().on_cancel()
        self.force_update_purchase_order_received_qty()

    def force_update_purchase_order_received_qty(self):
        purchase_order_items = set()
        purchase_orders = set()

        for row in self.items:
            if row.purchase_order_item:
                purchase_order_items.add(row.purchase_order_item)

            if row.purchase_order:
                purchase_orders.add(row.purchase_order)

        for po_detail in purchase_order_items:
            received_qty = frappe.db.sql("""
                select ifnull(sum(pri.received_qty), 0)
                from `tabPurchase Receipt Item` pri
                join `tabPurchase Receipt` pr on pr.name = pri.parent
                where pri.purchase_order_item = %s
                and pri.docstatus = 1
                and pr.docstatus = 1
                and ifnull(pr.is_return, 0) = 0
            """, po_detail)[0][0]

            frappe.db.set_value(
                "Purchase Order Item",
                po_detail,
                "received_qty",
                received_qty,
                update_modified=False
            )

            po_name = frappe.db.get_value("Purchase Order Item", po_detail, "parent")
            if po_name:
                purchase_orders.add(po_name)

        for po_name in purchase_orders:
            po = frappe.get_doc("Purchase Order", po_name)

            total_qty = sum(float(row.qty or 0) for row in po.items)
            total_received_qty = sum(float(row.received_qty or 0) for row in po.items)

            per_received = (total_received_qty / total_qty) * 100 if total_qty else 0

            frappe.db.set_value(
                "Purchase Order",
                po_name,
                {
                    "per_received": per_received
                },
                update_modified=False
            )

            po.reload()
            po.set_status(update=True)
            po.db_update()