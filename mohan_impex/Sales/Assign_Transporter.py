import frappe

def on_submit(doc, method):
    if not doc.pick_list:
        return

    selected_transporter = next(
        (t.transporter_name for t in doc.transporters if t.select == 1),
        None
    )

    if selected_transporter:
        frappe.db.set_value("Pick List", doc.pick_list, "custom_transporter_name", selected_transporter)
