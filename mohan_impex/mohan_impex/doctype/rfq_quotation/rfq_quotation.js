frappe.ui.form.on("RFQ Quotation", {
	refresh(frm) {
		if (frm.doc.workflow_state === "Transporter Assigned") {
			frm.add_custom_button(__("Update Pick List"), () => {
				update_pick_from_rfq(frm);
			});
		}
	},
});

function update_pick_from_rfq(frm) {
	frappe.call({
		method: "frappe.client.set_value",
		args: {
			doctype: "Pick List",
			name: frm.doc.pick_list,
			fieldname: {
				custom_transporter_name: frm.doc.transporter || "",
				custom_driver: frm.doc.driver || "",
				custom_driver_name: frm.doc.driver_name || "",
				custom_contact_number: frm.doc.phone_number || "",
				custom_vehicle_number: frm.doc.vehicle_number || "",
				custom_transport_charges: frm.doc.quoted_amount || 0,
				custom_expected_delivery: frm.doc.expected_delivery || "",
				custom_remarks: frm.doc.remarks || "",
			},
		},
		freeze: true,
		freeze_message: __("Updating Pick List..."),
		callback: function () {
			frappe.msgprint(__("Pick List updated."));
		},
	});
}
