// frappe.ui.form.on("RFQ Quotation", {
// 	refresh(frm) {
// 		if (frm.doc.workflow_state === "Transporter Assigned") {
// 			frm.add_custom_button(__("Update Pick List"), () => {
// 				update_pick_from_rfq(frm);
// 			});
// 		}
// 	},
// });

// function update_pick_from_rfq(frm) {
// 	frappe.call({
// 		method: "frappe.client.set_value",
// 		args: {
// 			doctype: "Pick List",
// 			name: frm.doc.pick_list,
// 			fieldname: {
// 				custom_transporter_name: frm.doc.transporter || "",
// 				custom_driver: frm.doc.driver || "",
// 				custom_driver_name: frm.doc.driver_name || "",
// 				custom_contact_number: frm.doc.phone_number || "",
// 				custom_vehicle_number: frm.doc.vehicle_number || "",
// 				custom_transport_charges: frm.doc.quoted_amount || 0,
// 				custom_expected_delivery: frm.doc.expected_delivery || "",
// 				custom_remarks: frm.doc.remarks || "",
// 			},
// 		},
// 		freeze: true,
// 		freeze_message: __("Updating Pick List..."),
// 		callback: function () {
// 			frappe.msgprint(__("Pick List updated."));
// 		},
// 	});
// }

frappe.ui.form.on("RFQ Quotation", {
	refresh(frm) {
		const roles = frappe.user_roles || [];

		if (roles.includes("MI Transporter") && !roles.includes("System Manager")) {
			return;
		}

		if (frm.doc.docstatus === 1 && frm.doc.workflow_state === "Pending") {
			frm.add_custom_button(__("Assign Transporter"), () => {
				assign_transporter(frm);
			});
		}

		if (frm.doc.workflow_state === "Awaiting Final Assignment") {
			frm.add_custom_button(__("Update Pick List"), () => {
				update_pick_from_rfq(frm);
			});
		}
	},
});

function assign_transporter(frm) {
	frappe.call({
		method: "mohan_impex.linked_pick.assign_transporter_actions",
		args: { rfq_quotation_name: frm.doc.name },
		freeze: true,
		freeze_message: __("Processing..."),
		callback: (r) => {
			const res = r.message || {};
			frappe.msgprint({
				title: __("Success"),
				message: __("Transport RFQ: {0}<br>Status: {1}<br>Rejected: {2}", [
					res.transport_rfq || "-",
					res.status_applied || "-",
					(res.rejected_quotations || []).join(", ") || "-",
				]),
				indicator: "green",
			});
			frm.reload_doc();
		},
	});
}

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
