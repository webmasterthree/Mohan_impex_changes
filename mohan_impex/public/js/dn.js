
// frappe.ui.form.on("Delivery Note", {
// 	after_save(frm) {
// 		frappe.call({
// 			method: "mohan_impex.linked_pick.get_linked_pick_list",
// 			args: { delivery_note: frm.doc.name || "" },
// 			callback(r) {
// 				const res = r.message;
// 				if (!res) return;

// 				if (typeof res === "object" && res.status === "error") {
// 					console.error("Pick List Sync Error:", res.message);
// 					frappe.msgprint(res.message || __("Pick List Sync Error"));
// 					return;
// 				}

// 				const updates = {
// 					transporter: res.custom_transporter_name || "",
// 					driver: res.custom_driver || "",
// 					driver_name: res.custom_driver_name || "",
// 					vehicle_no: res.custom_vehicle_number || "",
// 					custom_transport_charges: res.custom_transport_charges ?? 0,
// 					custom_expected_delivery_: res.custom_expected_delivery || null,
// 					custom_remarks_: res.custom_remarks || "",
// 					custom_contact_number: res.custom_contact_number || "",
// 				};

// 				let changed = false;
// 				for (const f in updates) {
// 					if ((frm.doc[f] ?? "") !== (updates[f] ?? "")) {
// 						changed = true;
// 						break;
// 					}
// 				}
// 				if (!changed) return;

// 				frm.set_value(updates);
// 			},
// 		});
// 	},
// });


frappe.ui.form.on("Delivery Note", {
	refresh(frm) {
		set_item_code_filter(frm);
	},
	after_save(frm){
		sync_from_pick_list(frm); // ✅ same event (refresh) for both
	}
});

function set_item_code_filter(frm) {
	frm.fields_dict["items"].grid.get_field("item_code").get_query = function (doc, cdt, cdn) {
		const row = locals[cdt][cdn] || {};
		return {
			filters: [
				["Item", "has_variants", "=", 0],
				["Item", "is_sales_item", "=", 1],
				["Item", "variant_of", "=", row.item_template || ""],
			],
		};
	};
}

function sync_from_pick_list(frm) {
	if (!frm.doc.name) return; // only after save / existing doc

	frappe.call({
		method: "mohan_impex.linked_pick.get_linked_pick_list",
		args: { delivery_note: frm.doc.name },
		callback(r) {
			const res = r.message;
			if (!res) return;

			if (typeof res === "object" && res.status === "error") {
				console.error("Pick List Sync Error:", res.message);
				frappe.msgprint(res.message || __("Pick List Sync Error"));
				return;
			}

			const updates = {
				transporter: res.custom_transporter_name || "",
				driver: res.custom_driver || "",
				driver_name: res.custom_driver_name || "",
				vehicle_no: res.custom_vehicle_number || "",
				custom_transport_charges: res.custom_transport_charges ?? 0,
				custom_expected_delivery_: res.custom_expected_delivery || null,
				custom_remarks_: res.custom_remarks || "",
				custom_contact_number: res.custom_contact_number || "",
			};

			// prevent unnecessary writes / loops
			let changed = false;
			for (const f in updates) {
				if ((frm.doc[f] ?? "") !== (updates[f] ?? "")) {
					changed = true;
					break;
				}
			}
			if (!changed) return;

			frm.set_value(updates);
		},
	});
}
