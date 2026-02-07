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
def split_rejected_batches(pr_name):
    """
    Split rejected batches into a new Serial and Batch Bundle
    and update item qty fields accordingly
    """
    
    pr = frappe.get_doc("Purchase Receipt", pr_name)
    
    # Check if PR is draft
    if pr.docstatus != 0:
        frappe.throw("This function only works on Draft Purchase Receipts")
    
    result = {}
    today_date = getdate(today())

    for item in pr.items:

        if not item.serial_and_batch_bundle:
            continue

        old_bundle = frappe.get_doc(
            "Serial and Batch Bundle",
            item.serial_and_batch_bundle
        )

        rejected_entries = []
        accepted_entries = []
        
        accepted_qty_total = 0
        rejected_qty_total = 0

        # 1️⃣ Classify batches
        for entry in old_bundle.entries:

            if not entry.batch_no:
                accepted_entries.append(entry)
                accepted_qty_total += entry.qty
                continue

            expiry = frappe.db.get_value(
                "Batch", entry.batch_no, "expiry_date"
            )

            if expiry and expiry < today_date:
                rejected_entries.append(entry)
                rejected_qty_total += entry.qty
            else:
                accepted_entries.append(entry)
                accepted_qty_total += entry.qty

        # Skip if no rejected batches
        if not rejected_entries:
            continue

        # 2️⃣ Create NEW rejected bundle (DRAFT)
        new_bundle = frappe.new_doc("Serial and Batch Bundle")
        new_bundle.item_code = old_bundle.item_code
        new_bundle.voucher_type = old_bundle.voucher_type
        new_bundle.voucher_no = old_bundle.voucher_no
        new_bundle.warehouse = old_bundle.warehouse
        new_bundle.type_of_transaction = old_bundle.type_of_transaction
        new_bundle.company = old_bundle.company

        for e in rejected_entries:
            new_bundle.append("entries", {
                "batch_no": e.batch_no,
                "qty": e.qty,
                "warehouse": e.warehouse,
                "incoming_rate": getattr(e, 'incoming_rate', 0)
            })

        new_bundle.insert(ignore_permissions=True)

        # 3️⃣ Update OLD bundle (remove rejected, keep accepted)
        old_bundle.entries = []
        
        for e in accepted_entries:
            old_bundle.append("entries", {
                "batch_no": e.batch_no,
                "qty": e.qty,
                "warehouse": e.warehouse,
                "incoming_rate": getattr(e, 'incoming_rate', 0)
            })

        old_bundle.save(ignore_permissions=True)

        # 4️⃣ Update item table fields
        item.qty = accepted_qty_total  # ✅ Set accepted qty
        item.rejected_qty = rejected_qty_total  # ✅ Set rejected qty
        item.rejected_serial_and_batch_bundle = new_bundle.name  # ✅ Set rejected bundle

        # Store rejected bundle name for response
        result[item.name] = {
            "rejected_bundle": new_bundle.name,
            "accepted_qty": accepted_qty_total,
            "rejected_qty": rejected_qty_total
        }

    pr.save(ignore_permissions=True)
    frappe.db.commit()
    
    return result