import frappe

@frappe.whitelist()
def get_linked_pick_list(delivery_note: str):
    """
    Fetch Pick List linked to a Delivery Note via Delivery Note Item.against_pick_list
    and return required custom fields.
    """
    try:
        if not delivery_note:
            return None

        against_pick_list = frappe.db.get_value(
            "Delivery Note Item",
            {"parent": delivery_note},
            "against_pick_list"
        )

        if not against_pick_list:
            return None

        pl_doc = frappe.get_doc("Pick List", against_pick_list)

        # If you're not 100% sure about the fieldname, keep this safe pattern:
        def safe_get(doc, fieldname):
            return doc.get(fieldname) if doc.meta.has_field(fieldname) else None

        return {
            "name": pl_doc.name,
            "custom_transporter_name": safe_get(pl_doc, "custom_transporter_name"),
            "custom_driver": safe_get(pl_doc, "custom_driver"),
            "custom_driver_name": safe_get(pl_doc, "custom_driver_name"),
            "custom_vehicle_number": safe_get(pl_doc, "custom_vehicle_number"),
            "custom_transport_charges": safe_get(pl_doc, "custom_transport_charges"),
            "custom_expected_delivery": safe_get(pl_doc, "custom_expected_delivery"),
            "custom_remarks": safe_get(pl_doc, "custom_remarks"),
            "custom_contact_number": safe_get(pl_doc, "custom_contact_number"),
        }

    except Exception:
        frappe.log_error(
            title="Pick List Link Fetch Error",
            message=frappe.get_traceback()
        )
        return {"status": "error", "message": "Failed to fetch linked Pick List"}




def on_submit(doc, method):
	if not doc.pick_list:
		return

	# Update Pick List using parent fields from RFQ Quotation
	frappe.db.set_value("Pick List", doc.pick_list, {
		"custom_transporter_name": doc.transporter,
		"custom_driver": doc.driver,
		"custom_driver_name": doc.driver_name,
		"custom_contact_number": doc.phone_number,
		"custom_vehicle_number": doc.vehicle_number,
		"custom_transport_charges": doc.quoted_amount,
		"custom_expected_delivery": doc.expected_delivery,
		"custom_remarks": doc.remarks,
	})

	frappe.msgprint(f"Updated Pick List {doc.pick_list} with transporter details.")
