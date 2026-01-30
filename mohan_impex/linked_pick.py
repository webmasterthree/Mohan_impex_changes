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



# import frappe
# from frappe import _
# from mohan_impex.transporter import quotation_receive_status, mark_rejected

# def on_submit(doc, method=None):

# 	if doc.get("workflow_state") == "Assign Transporter":
# 		if doc.get("pick_list"):
# 			frappe.db.set_value(
# 				"Pick List",
# 				doc.pick_list,
# 				{
# 					"custom_transporter_name": doc.get("transporter"),
# 					"custom_driver": doc.get("driver"),
# 					"custom_driver_name": doc.get("driver_name"),
# 					"custom_contact_number": doc.get("phone_number"),
# 					"custom_vehicle_number": doc.get("vehicle_number"),
# 					"custom_transport_charges": doc.get("quoted_amount"),
# 					"custom_expected_delivery": doc.get("expected_delivery"),
# 					"custom_remarks": doc.get("remarks"),
# 				},
# 				update_modified=True,
# 			)
# 			frappe.msgprint(_("Pick List {0} updated.").format(doc.pick_list))
# 		else:
# 			frappe.msgprint(_("Pick List not found; not updated."))

# 	transport_rfq = doc.get("transport")
# 	if not transport_rfq:
# 		frappe.msgprint(_("Transport RFQ link not found; title not updated."))
# 		return

# 	rejected_names = mark_rejected(transport_rfq) or []
# 	for name in rejected_names:
# 		if name != doc.name:
# 			frappe.db.set_value(
# 				"RFQ Quotation",
# 				name,
# 				"workflow_state",
# 				"Rejected",
# 				update_modified=True
# 			)

# 	try:
# 		status_res = quotation_receive_status(transport_rfq) or {}
# 		status = status_res.get("status")
# 	except Exception:
# 		frappe.log_error(frappe.get_traceback(), "Transport RFQ Status Fetch Error")
# 		frappe.msgprint(_("Transport RFQ title not updated (status fetch failed)."))
# 		return

# 	if not status:
# 		frappe.msgprint(_("Transport RFQ title not updated (receive status not found)."))
# 		return

# 	try:
# 		frappe.db.set_value(
# 			"Transport RFQ",
# 			transport_rfq,
# 			"title",
# 			status,
# 			update_modified=True
# 		)
# 	except Exception:
# 		frappe.log_error(frappe.get_traceback(), "Transport RFQ Title Update Error")
# 		frappe.msgprint(_("Transport RFQ title not updated (db update failed)."))

import frappe
from mohan_impex.transporter import quotation_receive_status, mark_rejected


def update_transport_rfq_title_on_submit(doc, method=None):
    transport_rfq = doc.get("transport")
    if not transport_rfq:
        return

    try:
        status_res = quotation_receive_status(transport_rfq) or {}
        status = status_res.get("status")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Transport RFQ Status Fetch Error")
        return

    if not status:
        return

    try:
        frappe.db.set_value(
            "Transport RFQ",
            transport_rfq,
            "title",
            status,
            update_modified=True
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Transport RFQ Title Update Error")


def reject_other_quotations_on_submit(doc, method=None):
    transport_rfq = doc.get("transport")
    if not transport_rfq:
        return

    rejected_names = mark_rejected(transport_rfq) or []
    for name in rejected_names:
        if name != doc.name:
            frappe.db.set_value(
                "RFQ Quotation",
                name,
                "workflow_state",
                "Rejected",
                update_modified=True
            )



