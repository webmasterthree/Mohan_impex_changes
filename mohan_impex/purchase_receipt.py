import frappe
from frappe.utils import today, getdate

def validate(doc, event):
    pass
#     today_date = getdate(today())

#     for item in doc.items:
#         accepted_qty = 0
#         rejected_qty = 0

#         if not item.serial_and_batch_bundle:
#             item.qty = 0
#             item.rejected_qty = 0
#             continue

#         sbb = frappe.get_doc(
#             "Serial and Batch Bundle",
#             item.serial_and_batch_bundle
#         )

#         for entry in sbb.entries:
#             if not entry.batch_no:
#                 continue

#             expiry_date = frappe.db.get_value(
#                 "Batch",
#                 entry.batch_no,
#                 "expiry_date"
#             )

#             if not expiry_date:
#                 continue

#             # ✅ CORRECT LOGIC
#             if today_date > getdate(expiry_date):
#                 rejected_qty += entry.qty
#             else:
#                 accepted_qty += entry.qty

#         # ✅ set on child row
#         item.qty = accepted_qty
#         item.rejected_qty = rejected_qty




import frappe
from frappe.utils import getdate, today


@frappe.whitelist()
def split_rejected_batches(pr_name, rejected_warehouse=None, workflow_status=None):
    pr = frappe.get_doc("Purchase Receipt", pr_name)

    if not rejected_warehouse:
        frappe.throw("Rejected Warehouse is mandatory")

    if not frappe.db.exists("Warehouse", rejected_warehouse):
        frappe.throw(f"Warehouse {rejected_warehouse} does not exist")

    result = {}
    today_date = getdate(today())

    for item in pr.items:

        if not item.serial_and_batch_bundle:
            continue

        old_bundle = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)

        rejected_entries = []
        accepted_entries = []
        accepted_qty_total = 0
        rejected_qty_total = 0

        for entry in old_bundle.entries:
            if not entry.batch_no:
                accepted_entries.append(entry)
                accepted_qty_total += entry.qty
                continue

            expiry = frappe.db.get_value("Batch", entry.batch_no, "expiry_date")

            if expiry and expiry < today_date:
                rejected_entries.append(entry)
                rejected_qty_total += abs(entry.qty)
            else:
                accepted_entries.append(entry)
                accepted_qty_total += entry.qty

        if not rejected_entries:
            continue

        # ✅ Create new rejected bundle
        new_bundle = frappe.new_doc("Serial and Batch Bundle")
        new_bundle.item_code = old_bundle.item_code
        new_bundle.voucher_type = old_bundle.voucher_type
        new_bundle.voucher_no = old_bundle.voucher_no
        new_bundle.warehouse = rejected_warehouse
        new_bundle.type_of_transaction = old_bundle.type_of_transaction
        new_bundle.company = old_bundle.company

        for e in rejected_entries:
            new_bundle.append("entries", {
                "batch_no": e.batch_no,
                "qty": e.qty,
                "warehouse": rejected_warehouse,
                "incoming_rate": getattr(e, 'incoming_rate', 0)
            })

        new_bundle.insert(ignore_permissions=True)

        # ✅ FIX: Use .set() instead of direct assignment
        if accepted_entries:
            old_bundle.set("entries", [])
            for e in accepted_entries:
                old_bundle.append("entries", {
                    "batch_no": e.batch_no,
                    "qty": e.qty,
                    "warehouse": e.warehouse,
                    "incoming_rate": getattr(e, 'incoming_rate', 0)
                })
            old_bundle.save(ignore_permissions=True)
        else:
            # ✅ FIX: All batches rejected — delete old bundle instead of saving empty
            frappe.delete_doc("Serial and Batch Bundle", old_bundle.name, ignore_permissions=True)
            item.db_set('serial_and_batch_bundle', None, update_modified=False)

        item.db_set('qty', accepted_qty_total, update_modified=False)
        item.db_set('rejected_qty', rejected_qty_total, update_modified=False)
        item.db_set('rejected_serial_and_batch_bundle', new_bundle.name, update_modified=False)
        item.db_set('rejected_warehouse', rejected_warehouse, update_modified=False)

        result[item.name] = {
            "rejected_bundle": new_bundle.name,
            "accepted_qty": accepted_qty_total,
            "rejected_qty": rejected_qty_total,
            "rejected_warehouse": rejected_warehouse
        }

    if workflow_status:
        pr.db_set('workflow_state', workflow_status, update_modified=False)
        result['workflow_status'] = workflow_status

    frappe.db.commit()
    return result