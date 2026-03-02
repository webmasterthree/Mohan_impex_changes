// =========================
// PURCHASE RECEIPT CLIENT SCRIPT (Improved + New Rule)
// NEW RULE:
// If frm.doc.update_total_weightkg == 1
//   -> use frm.doc.updated_weight (KG) instead of frm.doc.custom_total_weight
// for calculating custom_total_labour_cost
// =========================

frappe.ui.form.on("Purchase Receipt", {
	// ✅ Single validate (merged)
	validate: async function (frm) {
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm); // ✅ will auto-pick correct weight now
		await check_shelf_and_set(frm);
	},

	// Recalculate labour cost when header fields are changed
	custom_labour_rate_per_ton: function (frm) {
		calculate_labour_cost(frm);
	},
	custom_total_weight: function (frm) {
		calculate_labour_cost(frm);
	},
	updated_weight: function (frm) {
		calculate_labour_cost(frm);
	},
	update_total_weightkg: function (frm) {
		calculate_labour_cost(frm);
	},
	custom_no_of_labour: function (frm) {
		calculate_labour_cost(frm);
	},
	custom_labour_rate: function (frm) {
		calculate_labour_cost(frm);
	},
	conversion_factor: function (frm) {
		calculate_labour_cost(frm);
	},
	additional_cost: function (frm) {
		calculate_labour_cost(frm);
	},

	onload: function (frm) {
		set_batch_query_filter(frm);

		// ✅ Ensure totals are correct on load as well
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm);

		if (frm.doc.docstatus === 1 && frm.doc.custom_total_labour_cost != 0) {
			frappe.call({
				method: "mohan_impex.misc_payment_entry.has_labour_payment",
				args: { grn: frm.doc.name },
				callback: function (r) {
					if (r.message === false) {
						frm.add_custom_button(
							__("Labour Payment Entry"),
							() => make_labour_payment_invoice(frm),
							__("Create")
						);
					}
				},
			});
		}

		if (frm.doc.docstatus === 1 && frm.doc.total_misc_amount != 0) {
			frappe.call({
				method: "mohan_impex.misc_payment_entry.has_misc_payment",
				args: { misc_expense: frm.doc.name },
				callback: function (r) {
					if (r.message === false) {
						frm.add_custom_button(
							__("Misc Payment Entry"),
							() => make_misc_payment_entry(frm),
							__("Create")
						);
					}
				},
			});
		}

		if (frm.doc.docstatus === 1 && frm.doc.transport_charges != 0) {
			frappe.call({
				method: "mohan_impex.misc_payment_entry.has_transporter_payment",
				args: { transporter_payment: frm.doc.name },
				callback: function (r) {
					if (r.message === false) {
						frm.add_custom_button(
							__("Transporter Payment Entry"),
							() => transporter_payment_entry(frm),
							__("Create")
						);
					}
				},
			});
		}
	},

	after_save: function (frm) {
		fetch_po_fields_and_set_on_pr(frm);

		// ✅ Keep totals consistent
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm);
	},

	miscellaneous_expenses_remove: function (frm, cdt, cdn) {
		update_total_misc_amount(frm);
	},

	refresh: function (frm) {
		// ✅ Ensure total weight and labour cost reflect latest grid state
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm);

		if (frappe.session.user === "Administrator") {
			frm.add_custom_button("Check Expired Batches", function () {
				calculate_accept_reject(frm);
			});
		}

		if (frm.doc.workflow_state === "Purchase Team Approval Pending") {
			frm.page.clear_actions_menu();
			frm.page.set_primary_action("Review", () => {
				calculate_accept_reject1(frm);
			});
		}
	},

	before_workflow_action: async function (frm) {
		if (frm.doc.workflow_state === "Complete GRN") {
			await calculate_accept_reject(frm);
		}
	},
});


// =========================
// PURCHASE RECEIPT ITEM TRIGGERS
// =========================

frappe.ui.form.on("Purchase Receipt Item", {
	qty: function (frm, cdt, cdn) {
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm);
	},

	// If your rejected qty field is different, replace rejected_qty with that fieldname
	rejected_qty: function (frm, cdt, cdn) {
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm);
	},

	conversion_factor: function (frm, cdt, cdn) {
		update_pre_unloading_status(frm);
		calculate_labour_cost(frm);
	},

	custom_manufacturing_date: function (frm, cdt, cdn) {
		calculate_remaining_shelf_life(frm, cdt, cdn);
	},

	custom_shelf_life_in_days: function (frm, cdt, cdn) {
		frappe.ui.form.trigger(cdt, cdn, "custom_manufacturing_date");
	},
});


// =========================
// Shelf Life calculation per row
// =========================

function calculate_remaining_shelf_life(frm, cdt, cdn) {
	let row = locals[cdt][cdn];

	if (row.custom_manufacturing_date && row.custom_shelf_life_in_days) {
		let mfg_date = frappe.datetime.str_to_obj(row.custom_manufacturing_date);
		let today = frappe.datetime.str_to_obj(frappe.datetime.now_date());

		let days_since_mfg = frappe.datetime.get_day_diff(today, mfg_date);
		let remaining_life = row.custom_shelf_life_in_days - days_since_mfg;

		frappe.model.set_value(cdt, cdn, "custom_remaining_shelf_life", remaining_life);

		if (remaining_life > 0) {
			frappe.model.set_value(cdt, cdn, "custom_purchase_team_approval", "Approved");
		} else {
			frappe.model.set_value(cdt, cdn, "custom_purchase_team_approval", "Pending");

			frappe.msgprint({
				title: __("Warning"),
				message: __("This item has expired! Purchase Team Approval is required."),
				indicator: "red",
			});
		}
	}

	update_pre_unloading_status(frm);
	calculate_labour_cost(frm);
}


// =========================
// Total Weight (custom_total_weight)
// =========================

function update_pre_unloading_status(frm) {
	let total_weight = (frm.doc.items || []).reduce((sum, item) => {
		let qty = flt(item.qty) + flt(item.rejected_qty);
		let factor = flt(item.conversion_factor || 1);
		return sum + qty * factor;
	}, 0);

	frm.set_value("custom_total_weight", total_weight);
	frm.refresh_fields(["custom_total_weight"]);
}


// =========================
// NEW: Decide which weight to use for labour calc
// =========================

function get_weight_for_labour_calc(frm) {
	// update_total_weightkg can be 1 / "1" / true depending on fieldtype
	const use_updated = cint(frm.doc.update_total_weightkg || 0) === 1;

	if (use_updated) {
		return flt(frm.doc.updated_weight || 0);
	}

	return flt(frm.doc.custom_total_weight || 0);
}


// =========================
// Labour Cost (uses get_weight_for_labour_calc)
// =========================

function calculate_labour_cost(frm) {
	// ✅ weight selection based on update_total_weightkg
	let total_weight = get_weight_for_labour_calc(frm);

	let labour_rate = flt(frm.doc.custom_labour_rate || 0);
	let factor = flt(frm.doc.conversion_factor || 1);
	let additional_cost = flt(frm.doc.additional_cost || 0);

	let total_cost = 0;

	// Primary formula
	if (total_weight && labour_rate) {
		total_cost = (total_weight * labour_rate) / factor + additional_cost;
	}

	// Fallback formula
	if (total_cost === 0) {
		let no_of_labour = flt(frm.doc.custom_no_of_labour || 0);
		let rate_per_ton = flt(frm.doc.custom_labour_rate_per_ton || 0);

		if (no_of_labour && rate_per_ton && total_weight) {
			total_cost = (no_of_labour * rate_per_ton * total_weight) / 1000;
		}
	}

	frm.set_value("custom_total_labour_cost", total_cost);
	frm.refresh_field("custom_total_labour_cost");
}


// =========================
// Batch filter
// =========================

function set_batch_query_filter(frm) {
	frm.fields_dict.items.grid.get_field("batch_no").get_query = function (doc, cdt, cdn) {
		const row = locals[cdt][cdn];
		let filters = { item: row.item_code };

		if (row.custom_select_brand) {
			filters.custom_brand = row.custom_select_brand;
		}
		return { filters };
	};
}


// =========================
// Labour Payment Invoice
// =========================

function make_labour_payment_invoice(frm) {
	frappe.model.with_doctype("Purchase Invoice", () => {
		const pi = frappe.model.get_new_doc("Purchase Invoice");

		set_invoice_header_from_pr(pi, frm.doc);
		add_labour_item_row(pi, frm.doc);

		frappe.set_route("Form", "Purchase Invoice", pi.name);
	});
}

function set_invoice_header_from_pr(pi, pr) {
	Object.assign(pi, {
		supplier: pr.contractors_name,
		grn: pr.name,
	});
}

function add_labour_item_row(pi, pr) {
	const labour_cost = flt(pr.custom_total_labour_cost || 0);

	if (!labour_cost) {
		frappe.msgprint(__("Total Labour Cost is zero. Please check before creating invoice."));
	}

	const row = frappe.model.add_child(pi, "Purchase Invoice Item", "items");
	Object.assign(row, {
		item_template: "Service Item",
		item_code: "LABOUR CHARGE",
		item_name: "LABOUR CHARGE",
		uom: "NOS",
		qty: 1,
		rate: labour_cost,
	});
}


// =========================
// Fetch ASN Details From PO
// =========================

function fetch_po_fields_and_set_on_pr(frm) {
	if (!frm.doc.items || frm.doc.items.length === 0) return;

	const po_in_item = frm.doc.items[0].purchase_order;
	if (!po_in_item) return;

	frappe.call({
		method: "mohan_impex.PR_Connection.get_linked_purchase_order",
		args: { purchase_receipt: frm.doc.name },
		callback: function (r) {
			if (!r.message) return;

			if (r.message.status === "error") {
				frappe.msgprint(__("Error fetching Purchase Order details: {0}", [r.message.message]));
				return;
			}

			const data = r.message;

			frm.set_value("custom_transporters_name", data.custom_transporter_name || "");
			frm.set_value("custom_vehicle_no__container_no", data.custom_vehiclecontainer_number || "");
			frm.set_value("assigned_driver", data.custom_driver_name || "");
			frm.set_value("driver_mobile_number", data.custom_driver_mobile_number || "");
			frm.set_value("lr_number", data.lr_no || "");
			frm.set_value("driver", data.driver || "");
			frm.set_value("transporter", data.transporter || "");
			frm.set_value("transport_charges",data.transport_charges || "");
			frm.set_value("remarks",data.remarks || "");
			frm.set_value("vehicle_no",data.custom_vehiclecontainer_number || "");

		},
	});
}


// =========================
// Misc Payment Entry
// =========================

function make_misc_payment_entry(frm) {
	frappe.call({
		method: "mohan_impex.misc_payment_entry.misc_payment_entry",
		args: { purchase_receipt: frm.doc.name },
		callback: function (r) {
			const data = r.message;

			if (!data) {
				frappe.msgprint(__("No data returned from server."));
				return;
			}

			if (!data.miscellaneous_expenses || !data.miscellaneous_expenses.length) {
				frappe.msgprint(__("No Miscellaneous Expenses found to create Purchase Invoice."));
				return;
			}

			frappe.model.with_doctype("Purchase Invoice", () => {
				const pi = frappe.model.get_new_doc("Purchase Invoice");

				pi.supplier = data.misc_supplier;
				pi.misc_expense = data.name;

				(data.miscellaneous_expenses || []).forEach((row) => {
					const pi_item = frappe.model.add_child(pi, "items");

					pi_item.item_template = row.misc_item_template;
					pi_item.item_code = row.item_name;
					pi_item.item_name = row.item_details;
					pi_item.qty = row.qty;
					pi_item.uom = row.uom;
					pi_item.rate = row.rate || 0;
					pi_item.amount = row.amount || 0;
				});

				frappe.set_route("Form", "Purchase Invoice", pi.name);
			});
		},
	});
}


// =========================
// Misc Expense Child Table calc
// =========================

frappe.ui.form.on("Miscellaneous Expense Items", {
	qty(frm, cdt, cdn) {
		update_item_amount_and_total(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		update_item_amount_and_total(frm, cdt, cdn);
	},
});

function update_item_amount_and_total(frm, cdt, cdn) {
	const row = locals[cdt][cdn];

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


// =========================
// Transporter Payment Entry
// =========================

function transporter_payment_entry(frm) {
	if (!frm.doc.transporter) {
		frappe.msgprint(__("Please set Transporter before creating Transport Payment Invoice."));
		return;
	}

	if (!frm.doc.transport_charges) {
		frappe.msgprint(__("Transport Charges is zero or not set."));
		return;
	}

	frappe.model.with_doctype("Purchase Invoice", () => {
		const pi = frappe.model.get_new_doc("Purchase Invoice");

		pi.supplier = frm.doc.transporter;
		pi.company = frm.doc.company;
		pi.transporter_payment = frm.doc.name;

		const row = frappe.model.add_child(pi, "items");
		row.item_template = "Service Item";
		row.item_code = "Transport-Services";
		row.item_name = "Transport-Services";
		row.description = `Transport charges for ${frm.doc.name}`;
		row.uom = "NOS";
		row.qty = 1;
		row.rate = frm.doc.transport_charges || 0;

		frappe.set_route("Form", "Purchase Invoice", pi.name);
	});
}


// =========================
// Shelf Issue Flag -> custom_rejected_qty on PR (Yes/No)
// =========================

async function check_shelf_and_set(frm) {
	let issue = await has_shelf_issue(frm);

	if (issue) {
		await frm.set_value("custom_rejected_qty", "Yes");
	} else {
		await frm.set_value("custom_rejected_qty", "No");
	}

	frm.refresh_field("custom_rejected_qty");
}

async function has_shelf_issue(frm) {
	const today = frappe.datetime.get_today();

	for (let item of frm.doc.items || []) {
		// CASE 1: Serial and Batch Bundle row
		if (item.serial_and_batch_bundle) {
			let sbb = await frappe.db.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle);
			let shelf_days = sbb.custom_shelf_life_in_days || 0;

			for (let entry of sbb.entries || []) {
				if (!entry.batch_no || !entry.qty) continue;
				if (entry.qty < 0) continue;

				let batch = await frappe.db.get_value("Batch", entry.batch_no, "expiry_date");
				let expiry_date = batch?.message?.expiry_date;

				if (expiry_date && expiry_date < today) return true;

				let remaining = entry.custom_remaining_shelf_life || 0;
				let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;

				if (percent < 25) return true;
			}
		}

		// CASE 2: Direct batch_no row
		else if (item.use_serial_batch_fields && item.batch_no) {
			let batch_doc = await frappe.db.get_doc("Batch", item.batch_no);

			let expiry_date = batch_doc?.expiry_date;
			let manufacturing_date = batch_doc?.manufacturing_date;

			if (expiry_date && expiry_date < today) return true;

			if (expiry_date && manufacturing_date) {
				let exp = frappe.datetime.str_to_obj(expiry_date);
				let mfg = frappe.datetime.str_to_obj(manufacturing_date);
				let tod = frappe.datetime.str_to_obj(today);

				let total_shelf_days = frappe.datetime.get_diff(exp, mfg);
				let remaining_days = frappe.datetime.get_diff(exp, tod);

				let percent = total_shelf_days ? (remaining_days / total_shelf_days) * 100 : 0;
				if (percent < 25) return true;
			}
		}
	}

	return false;
}


// =========================
// Dialog & Workflow: calculate_accept_reject
// (Kept your structure; shelf-life percent fixed)
// =========================

async function calculate_accept_reject(frm) {
	const today = frappe.datetime.get_today();
	let dialog_data = [];
	let has_issue = false;

	for (let item of frm.doc.items || []) {
		if (!item.serial_and_batch_bundle) continue;

		let accepted_qty = 0;
		let rejected_qty = 0;
		let lt25_qty = 0;
		let gt25_qty = 0;

		let sbb = await frappe.db.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle);
		let shelf_days = sbb.custom_shelf_life_in_days || 0;

		for (let entry of (sbb.entries || [])) {
			if (!entry.batch_no || !entry.qty) continue;

			let batch = await frappe.db.get_value("Batch", entry.batch_no, "expiry_date");
			let expiry_date = batch?.message?.expiry_date;

			if (expiry_date && expiry_date < today) {
				rejected_qty += entry.qty;
				continue;
			}

			accepted_qty += entry.qty;

			let remaining = entry.custom_remaining_shelf_life || 0;
			let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;

			if (percent < 25) lt25_qty += entry.qty;
			else gt25_qty += entry.qty;
		}

		dialog_data.push({
			item_code: item.item_code,
			serial_and_batch_bundle: item.serial_and_batch_bundle,
			lt25_qty,
			gt25_qty,
			accepted_qty,
			rejected_qty,
		});

		if (rejected_qty > 0 || lt25_qty > 0) has_issue = true;
	}

	if (has_issue) {
		open_result_dialog(dialog_data, frm);
		return false;
	}

	return true;
}

async function open_result_dialog(data, frm) {
	let d = new frappe.ui.Dialog({
		title: "Review Items",
		size: "large",
		fields: [
			{
				fieldname: "items",
				fieldtype: "Table",
				cannot_add_rows: true,
				cannot_delete_rows: true,
				in_place_edit: false,
				data: data,
				fields: [
					{ fieldname: "item_code", fieldtype: "Data", label: "Item", in_list_view: 1, read_only: 1 },
					{ fieldname: "lt25_qty", fieldtype: "Float", label: "Shelf Life Less Than 25% QTY", in_list_view: 1, read_only: 1 },
					{ fieldname: "gt25_qty", fieldtype: "Float", label: "Shelf Life Greater Than 25% QTY", in_list_view: 1, read_only: 1 },
					{ fieldname: "accepted_qty", fieldtype: "Float", label: "Accepted QTY", in_list_view: 1, read_only: 1 },
					{ fieldname: "rejected_qty", fieldtype: "Float", label: "Expiry QTY", in_list_view: 1, read_only: 1 },
					{
						fieldname: "serial_and_batch_bundle",
						fieldtype: "Link",
						label: "Serial and Batch Bundle",
						options: "Serial and Batch Bundle",
						in_list_view: 1,
						read_only: 1,
					},
				],
			},
		],

		primary_action_label: "Send for Approval",
		primary_action: async function () {
			d.hide();
			try {
				frm.set_value("workflow_state", "Purchase Team Approval Pending");
				await frm.save();

				frappe.show_alert({ message: __("Sent for approval successfully"), indicator: "green" });
			} catch (e) {
				console.error("Error:", e);
				frappe.msgprint({ title: __("Error"), message: e.message, indicator: "red" });
			}
		},
	});

	d.show();
	d.fields_dict.items.grid.refresh();

	$(d.$wrapper).find(".modal-dialog").css({
		"max-width": "1500px",
		width: "100%",
	});
}


// =========================
// Review Dialog 2 (Kept as-is)
// =========================

async function calculate_accept_reject1(frm) {
	const today = frappe.datetime.get_today();
	let dialog_data = [];
	let has_rejected_items = false;

	for (let item of frm.doc.items || []) {
		if (!item.serial_and_batch_bundle) continue;

		let accepted_qty = 0;
		let rejected_qty = 0;
		let lt25_qty = 0;
		let gt25_qty = 0;

		let sbb = await frappe.db.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle);
		let shelf_days = sbb.custom_shelf_life_in_days || 0;

		for (let entry of (sbb.entries || [])) {
			if (!entry.batch_no || !entry.qty) continue;

			let batch = await frappe.db.get_value("Batch", entry.batch_no, "expiry_date");
			let expiry_date = batch?.message?.expiry_date;

			if (expiry_date && expiry_date < today) {
				rejected_qty += entry.qty;
				continue;
			}

			accepted_qty += entry.qty;

			let remaining = entry.custom_remaining_shelf_life || 0;
			let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;

			if (percent < 25) lt25_qty += entry.qty;
			else gt25_qty += entry.qty;
		}

		if (rejected_qty > 0) has_rejected_items = true;

		dialog_data.push({
			name: item.item_name,
			item_code: item.item_code,
			item_name: item.name,
			lt25_qty,
			gt25_qty,
			accepted_qty,
			rejected_qty,
			serial_and_batch_bundle: item.serial_and_batch_bundle,
		});
	}

	open_result_dialog1(dialog_data, frm, has_rejected_items);
}

function open_result_dialog1(data, frm, has_rejected_items) {
	let dialog_fields = [];

	if (has_rejected_items) {
		dialog_fields.push({
			fieldname: "rejected_warehouse",
			fieldtype: "Link",
			label: "Rejected Warehouse",
			options: "Warehouse",
			reqd: 1,
			description: "Select warehouse for rejected batches",
		});
		dialog_fields.push({ fieldname: "section_break", fieldtype: "Section Break" });
	}

	dialog_fields.push({
		fieldname: "items",
		fieldtype: "Table",
		label: "Item Summary",
		cannot_add_rows: true,
		in_place_edit: false,
		fields: [
			{ fieldname: "name", fieldtype: "Data", label: "Item Name", in_list_view: 1, read_only: 1 },
			{ fieldname: "item_code", fieldtype: "Data", label: "Item Code", read_only: 1 },
			{ fieldname: "lt25_qty", fieldtype: "Float", label: "Shelf Life Less Then 25% QTY", in_list_view: 1, read_only: 1 },
			{ fieldname: "gt25_qty", fieldtype: "Float", label: "Shelf Life Greater Than 25% QTY", in_list_view: 1, read_only: 1 },
			{ fieldname: "accepted_qty", fieldtype: "Float", label: "Accepted Total Qty", in_list_view: 1, read_only: 1 },
			{ fieldname: "rejected_qty", fieldtype: "Float", label: "Expiry Qty", in_list_view: 1, read_only: 1 },
			{
				fieldname: "serial_and_batch_bundle",
				fieldtype: "Link",
				label: "Serial and Batch Bundle",
				options: "Serial and Batch Bundle",
				read_only: 1,
			},
		],
	});

	let d = new frappe.ui.Dialog({
		title: "Accepted / Rejected Qty (Expiry Based)",
		size: "large",
		fields: dialog_fields,

		primary_action_label: "Approve",
		primary_action: async function () {
			await process_split_batches(d, frm, "Approved", has_rejected_items);
		},

		secondary_action_label: "Reject",
		secondary_action: async function () {
			await process_split_batches(d, frm, "Rejected", has_rejected_items);
		},
	});

	d.show();

	d.fields_dict.items.df.data = data;
	d.fields_dict.items.grid.refresh();

	$(d.$wrapper).find(".modal-dialog").css({
		"max-width": "1500px",
		width: "100%",
	});
}

async function process_split_batches(dialog, frm, workflow_status, has_rejected_items) {
	let values = dialog.get_values();

	if (has_rejected_items && !values.rejected_warehouse) {
		frappe.msgprint({
			title: __("Required"),
			message: __("Please select Rejected Warehouse"),
			indicator: "red",
		});
		return;
	}

	dialog.hide();

	if (!has_rejected_items) {
		frappe.show_alert({ message: __("Processing..."), indicator: "blue" });

		try {
			await frappe.call({
				method: "frappe.client.set_value",
				args: {
					doctype: frm.doc.doctype,
					name: frm.doc.name,
					fieldname: "workflow_state",
					value: "Approved",
				},
			});

			frappe.show_alert({ message: __("Approved successfully!"), indicator: "green" });
			frm.reload_doc();
		} catch (error) {
			frappe.msgprint({
				title: __("Error"),
				message: error.message || __("Failed to update workflow"),
				indicator: "red",
			});
		}

		return;
	}

	frappe.show_alert({ message: __("Processing..."), indicator: "blue" });

	try {
		let result = await frappe.call({
			method: "mohan_impex.purchase_receipt.split_rejected_batches",
			args: {
				pr_name: frm.doc.name,
				rejected_warehouse: values.rejected_warehouse || null,
				workflow_status: workflow_status,
			},
		});

		if (result.message) {
			for (let item_name in result.message) {
				let item_row = (frm.doc.items || []).find((i) => i.name === item_name);

				if (item_row) {
					frappe.model.set_value(
						item_row.doctype,
						item_row.name,
						"rejected_serial_and_batch_bundle",
						result.message[item_name].rejected_bundle
					);

					frappe.model.set_value(
						item_row.doctype,
						item_row.name,
						"rejected_warehouse",
						result.message[item_name].rejected_warehouse
					);
				}
			}

			if (result.message.workflow_status) {
				frm.set_value("workflow_state", result.message.workflow_status);
			}

			frm.refresh_field("items");

			frappe.show_alert({
				message: __(
					workflow_status === "Approved" ? "Approved successfully!" : "Rejected successfully!"
				),
				indicator: workflow_status === "Approved" ? "green" : "orange",
			});

			frm.reload_doc();
		}
	} catch (error) {
		frappe.msgprint({
			title: __("Error"),
			message: error.message || __("Failed to process"),
			indicator: "red",
		});
	}
}
