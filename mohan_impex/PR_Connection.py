import frappe

@frappe.whitelist()
def get_linked_purchase_order(purchase_receipt):
    try:
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
