frappe.ui.form.on("Delivery Note", {
	validate(frm) {
		update_total_weight(frm);
		calculate_labour_cost(frm);
	},

	custom_labour_rate_per_ton(frm) {
		calculate_labour_cost(frm);
	},
	custom_total_weight(frm) {
		calculate_labour_cost(frm);
	},
	custom_no_of_labour(frm) {
		calculate_labour_cost(frm);
	},
	custom_labour_rate(frm) {
		calculate_labour_cost(frm);
	},

	refresh(frm) {
		set_item_code_filter(frm);

		// ✅ Manual sync button (no auto-sync on after_save)
		if (!frm.is_new()) {
			frm.add_custom_button(
				__("Sync Transporter"),
				() => sync_from_pick_list(frm, true),
				__("Actions")
			);
		}
	},

	miscellaneous_expenses_remove(frm) {
		update_total_misc_amount(frm);
	},
});

// -----------------------------
// Total Weight
// -----------------------------
function update_total_weight(frm) {
	const total_weight = (frm.doc.items || []).reduce((sum, item) => {
		return sum + flt(item.stock_qty || 0);
	}, 0);

	frm.set_value("custom_total_weight", total_weight);
	frm.refresh_fields(["custom_total_weight"]);
}

// -----------------------------
// Labour Cost Calculation
// -----------------------------
function calculate_labour_cost(frm) {
	const total_weight = flt(frm.doc.custom_total_weight || 0);
	const labour_rate = flt(frm.doc.custom_labour_rate || 0);
	const factor = flt(frm.doc.conversion_factor || 1);
	const additional_cost = flt(frm.doc.additional_cost || 0);

	let total_cost = 0;

	// Primary formula
	if (total_weight && labour_rate) {
		total_cost = (total_weight * labour_rate) / factor + additional_cost;
	}

	// Fallback formula
	if (total_cost === 0) {
		const no_of_labour = flt(frm.doc.custom_no_of_labour || 0);
		const rate_per_ton = flt(frm.doc.custom_labour_rate_per_ton || 0);

		if (no_of_labour && rate_per_ton && total_weight) {
			total_cost = (no_of_labour * rate_per_ton * total_weight) / 1000;
		}
	}

	frm.set_value("custom_total_labour_cost", total_cost);
}

// -----------------------------
// Item Code Filter (no variants, sales item, template-based)
// -----------------------------
function set_item_code_filter(frm) {
	const grid = frm.fields_dict?.items?.grid;
	if (!grid) return;

	grid.get_field("item_code").get_query = function (doc, cdt, cdn) {
		const row = locals[cdt]?.[cdn] || {};

		// If template not selected, allow all non-variant sales items
		const filters = [
			["Item", "has_variants", "=", 0],
			["Item", "is_sales_item", "=", 1],
		];

		if (row.item_template) {
			filters.push(["Item", "variant_of", "=", row.item_template]);
		}

		return { filters };
	};
}

// -----------------------------
// Sync from Pick List (manual button)
// -----------------------------
function sync_from_pick_list(frm, show_msg = false) {
	if (!frm.doc.name) {
		if (show_msg) frappe.msgprint(__("Please save the Delivery Note first."));
		return;
	}

	frappe.call({
		method: "mohan_impex.linked_pick.get_linked_pick_list",
		args: { delivery_note: frm.doc.name },
		freeze: true,
		freeze_message: __("Syncing transporter details..."),
		callback(r) {
			const res = r.message;
			if (!res) {
				if (show_msg) frappe.msgprint(__("No linked Pick List data found."));
				return;
			}

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

			// Prevent unnecessary writes / loops
			let changed = false;
			for (const f in updates) {
				if ((frm.doc[f] ?? "") !== (updates[f] ?? "")) {
					changed = true;
					break;
				}
			}

			if (!changed) {
				if (show_msg) frappe.show_alert({ message: __("Already up to date."), indicator: "green" });
				return;
			}

			frm.set_value(updates).then(() => {
				frm.refresh_fields(Object.keys(updates));
				if (show_msg) frappe.msgprint(__("Transporter details synced from Pick List."));
			});
		},
	});
}

// -----------------------------
// Misc child table amount + total
// -----------------------------
frappe.ui.form.on("Miscellaneous Expense Items", {
	qty(frm, cdt, cdn) {
		update_item_amount_and_total(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		update_item_amount_and_total(frm, cdt, cdn);
	},
});

function update_item_amount_and_total(frm, cdt, cdn) {
	const row = locals[cdt]?.[cdn];
	if (!row) return;

	const qty = flt(row.qty) || 0;
	const rate = flt(row.rate) || 0;
	const amt_precision = typeof precision === "function" ? precision("amount", row) : 2;

	const amount = flt(qty * rate, amt_precision);
	frappe.model.set_value(cdt, cdn, "amount", amount);

	update_total_misc_amount(frm, amt_precision);
}

function update_total_misc_amount(frm, amt_precision) {
	const precision_to_use =
		typeof precision === "function"
			? precision("total_misc_amount", frm.doc)
			: amt_precision || 2;

	let total = 0;
	(frm.doc.miscellaneous_expenses || []).forEach((d) => {
		total += flt(d.amount) || 0;
	});

	frm.set_value("total_misc_amount", flt(total, precision_to_use));
	frm.refresh_field("total_misc_amount");
}