frappe.ui.form.on("Transport RFQ", {
	onload(frm) {
		frappe.call({
			method: "mohan_impex.user_roles.transporter_user",
			callback(r) {
				const is_transporter_user = !!r.message;

				frm.toggle_display("transporters", !is_transporter_user);
                frm.toggle_display("pick_list",!is_transporter_user);

				if (!is_transporter_user) return;

				let existing_rows = (frm.doc.transporter_details || []).filter(
					(row) => row.transporter === r.message
				);

				if (existing_rows.length === 1 && (frm.doc.transporter_details || []).length === 1) {
					return;
				}

				frm.clear_table("transporter_details");
				let row = frm.add_child("transporter_details");

				if (existing_rows.length) {
					Object.assign(row, existing_rows[0]);
				} else {
					row.transporter = r.message;
				}

				frm.refresh_field("transporter_details");
			},
		});
	},
});
