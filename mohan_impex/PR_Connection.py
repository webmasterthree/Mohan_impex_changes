# import frappe

# @frappe.whitelist()
# def get_linked_purchase_order(purchase_receipt):
#     """
#     Fetch the linked Purchase Order for a given Purchase Receipt.
#     """
#     try:
#         purchase_order = frappe.db.get_value(
#             "Purchase Receipt Item",
#             {"parent": purchase_receipt},
#             "purchase_order"
#         )

#         return purchase_order if purchase_order else None

#     except Exception as e:
#         frappe.log_error(f"Error fetching linked PO: {str(e)}", "Purchase API Error")
#         return {"status": "error", "message": str(e)}


import frappe

@frappe.whitelist()
def get_linked_purchase_order(purchase_receipt):
    try:
        # Get linked Purchase Order name from Purchase Receipt Item
        purchase_order = frappe.db.get_value(
            "Purchase Receipt Item",
            {"parent": purchase_receipt},
            "purchase_order"
        )

        if not purchase_order:
            return None

        po_doc = frappe.get_doc("Purchase Order", purchase_order)

        return {
            "name": po_doc.name,
            "custom_transporter_name": po_doc.custom_transporter_name,
            "custom_vehiclecontainer_number": po_doc.custom_vehiclecontainer_number,
            "custom_expected_arrival_date_": po_doc.custom_expected_arrival_date_,
            "custom_driver_name": po_doc.custom_driver_name,
            "custom_driver_mobile_number": po_doc.custom_driver_mobile_number,
            "lr_no": po_doc.lr_no,
        }

    except Exception as e:
        frappe.log_error(f"Error fetching linked PO: {str(e)}", "Purchase API Error")
        return {"status": "error", "message": str(e)}




# pick list connection
@frappe.whitelist()
def get_linked_pick_list(delivery_note):
    try:
        purchase_order = frappe.db.get_value(
            "Delivery Note Item",
            {"parent": delivery_note},
            "pick_list"
        )

        if not pick_list:
            return None

        po_doc = frappe.get_doc("Pick List", pick_list)

        return {
            "name": po_doc.name,
            "custom_transporter_name": po_doc.custom_transporter_name,
            "custom_driver": po_doc.custom_driver,
            "custom_driver_name": po_doc.custom_driver_name,
            "custom_vehicle_number": po_doc.custom_vehicle_number,
            "custom_transport_charges": po_doc.custom_transport_charges,
            "custom_expected_delivery": po_doc.custom_expected_delivery,
            "custom_remarks": po_doc.custom_remarks,
            "custom_contact_number":po_doc.custom_contact_number
            
        }

    except Exception as e:
        frappe.log_error(f"Error fetching linked PO: {str(e)}", "Purchase API Error")
        return {"status": "error", "message": str(e)}
