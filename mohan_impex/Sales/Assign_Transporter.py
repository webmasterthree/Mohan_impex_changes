import frappe

def on_submit(doc, method):
    if not doc.pick_list:
        return

    selected = next(
        (t for t in doc.transporters if t.select == 1),
        None
    )

    if selected:
        frappe.db.set_value("Pick List", doc.pick_list, {
            "custom_transporter_name": selected.transporter_name,
            "custom_driver":selected.driver,
            "custom_driver_name": selected.driver_name,
            "custom_contact_number": selected.phone_number,
            "custom_vehicle_number": selected.vehicle_number,
            "custom_transport_charges": selected.quoted_amount,
            "custom_expected_delivery": selected.expected_delivery,
            "custom_remarks": selected.remarks
        })

        frappe.msgprint(f"Updated Pick List {doc.pick_list} with transporter details.")



# import frappe

# def on_submit(doc, method):
#     if not doc.pick_list:
#         return

#     selected_transporter = next(
#         (t.transporter_name for t in doc.transporters if t.select == 1),
#         None
#     )

#     if selected_transporter:
#         frappe.db.set_value("Pick List", doc.pick_list, "custom_transporter_name", selected_transporter)
