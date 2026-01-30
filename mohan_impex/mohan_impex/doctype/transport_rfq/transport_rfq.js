frappe.ui.form.on("Transport RFQ", {
	refresh(frm) {
		if (frm.doc.docstatus != 1) return;

		const user_email = frappe.session.user;

		frappe.call({
			method: "mohan_impex.user_roles.is_created",
			args: {
				transport: frm.doc.name,
				user_email: user_email,
			},
			callback: function (r) {
				const already_created = !!r.message;

				if (!already_created) {
					frm.add_custom_button(__("Create Quotation"), () => {
						create_quotation(frm);
					});
				}
			},
		});
	},
});

function create_quotation(frm) {
	const user_email = frappe.session.user;

	frappe.call({
		method: "mohan_impex.user_roles.transporter_name",
		args: {
			user_email: user_email,
		},
		callback: function (r) {
			const data = (r.message && r.message.length) ? r.message[0] : null;

			frappe.model.with_doctype("RFQ Quotation", () => {
				const qtn = frappe.model.get_new_doc("RFQ Quotation");

				qtn.transporter = data ? (data.name || "") : "";
				qtn.transporter_name = data ? (data.supplier_name || data.name || "") : "";

				qtn.transport = frm.doc.name;
				qtn.from_location = frm.doc.from_location;
				qtn.to_location = frm.doc.to_location;
				qtn.vehicle_type = frm.doc.vehicle_type;
				qtn.total_weightin_kg = frm.doc.total_weightin_kg;
				qtn.pick_list = frm.doc.pick_list;

				qtn.locations = [];
				(frm.doc.locations || []).forEach((row) => {
					const child = frappe.model.add_child(qtn, null, "locations");
					Object.assign(child, row);
				});

				frappe.set_route("Form", "RFQ Quotation", qtn.name);
			});
		},
	});
}
