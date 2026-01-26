frappe.ui.form.on("Transport RFQ", {
	refresh(frm) {
		if (frm.doc.docstatus == "1") {
			frm.add_custom_button(__("Create Quotation"), () => {
				create_quotation(frm);
			});
		}
 	}
});

function create_quotation(frm) {
	frappe.model.with_doctype("RFQ Quotation", () => {
		const qtn = frappe.model.get_new_doc("RFQ Quotation");
        qtn.transporter = frm.doc.transporter_details[0].transporter;
        qtn.quoted_amount = frm.doc.transporter_details[0].quoted_amount;
        qtn.expected_delivery = frm.doc.transporter_details[0].expected_delivery;
        qtn.remarks = frm.doc.transporter_details[0].remarks;
		qtn.transport = frm.doc.name;
		qtn.from_location = frm.doc.from_location;
		qtn.to_location = frm.doc.to_location;
		qtn.vehicle_type = frm.doc.vehicle_type;
        qtn.total_weightin_kg = frm.doc.total_weightin_kg;
        qtn.pick_list = frm.doc.pick_list;
		qtn.locations = [];
		(frm.doc.locations || []).forEach((r) => {
			const child = frappe.model.add_child(qtn, null, "locations");
			Object.assign(child, r);
		});
		frappe.set_route("Form", "RFQ Quotation", qtn.name);
	});
}

 