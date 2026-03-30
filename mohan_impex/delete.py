import frappe

@frappe.whitelist()
def delete_all_serial_batch_bundle():

    names = frappe.db.get_all(
        "Serial and Batch Bundle",
        pluck="name"
    )

    deleted = []
    failed = []

    for name in names:
        try:
            doc = frappe.get_doc("Serial and Batch Bundle", name)

            # 🔥 Step 1: Cancel if submitted
            if doc.docstatus == 1:
                doc.cancel()

            # 🔥 Step 2: Delete
            frappe.delete_doc("Serial and Batch Bundle", name, force=1)

            deleted.append(name)

        except Exception as e:
            failed.append({"name": name, "error": str(e)})

    return {
        "total": len(names),
        "deleted": len(deleted),
        "failed": failed[:10]  # show only first 10 errors
    }