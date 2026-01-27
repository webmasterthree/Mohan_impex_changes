frappe.ui.form.on("Full and Final Statement", {
	refresh: function (frm) {
		frm.events.set_queries(frm, "payables");
		frm.events.set_queries(frm, "receivables");
		buy_out(frm)
	},
	set_queries: function (frm, type) {
		frm.set_query("reference_document_type", type, function () {
			return {
				query: "mohan_impex.full_and_final_statement.get_reference_doctypes"
			};
		});

		let filters = {};
		frm.set_query("reference_document", type, function (doc, cdt, cdn) {
			let fnf_doc = frappe.get_doc(cdt, cdn);
			frappe.model.with_doctype(fnf_doc.reference_document_type, function () {
				if (frappe.model.is_tree(fnf_doc.reference_document_type)) {
					filters["is_group"] = 0;
				}
				if (frappe.model.is_submittable(fnf_doc.reference_document_type)) {
					filters["docstatus"] = ["!=", 2];
				}
				if (frappe.meta.has_field(fnf_doc.reference_document_type, "company")) {
					filters["company"] = frm.doc.company;
				}
				if (frappe.meta.has_field(fnf_doc.reference_document_type, "employee")) {
					filters["employee"] = frm.doc.employee;
				}
				if (fnf_doc.reference_document_type === "Leave Encashment") {
					filters["status"] = "Unpaid";
					filters["pay_via_payment_entry"] = 1;
				}
			});
			return {
				filters: filters,
			};
		});
	}
});

frappe.ui.form.on("Full and Final Outstanding Statement", {
	reference_document: function (frm, cdt, cdn) {
		const child = locals[cdt][cdn];
		if (child.reference_document_type && child.reference_document) {
			frappe.call({
				method: "mohan_impex.full_and_final_statement.get_account_and_amount",
				args: {
					ref_doctype: child.reference_document_type,
					ref_document: child.reference_document,
					company: frm.doc.company,
				},
				callback: function (r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, "account", r.message[0]);
						frappe.model.set_value(cdt, cdn, "amount", r.message[1]);
					}
				},
			});
		}
	}
});


function buy_out(frm){
	if (!frm.is_new()) {
		frm.add_custom_button(__('Buy Out'), function() {
			frappe.call({
				method: "mohan_impex.full_and_final_statement.get_buyout_doc",
				args: {
					employee: frm.doc.employee
				},
				callback: function(r) {

					if (!r.message) {
						frappe.msgprint("No Buyout doc found");
						return;
					}

					let doc = r.message;
					let doctype = "Notice Period Buyout";
					let name = doc.name;

					let amount = doc.amount || 0;

					// Decide which child table
					let child_table_field = null;

					if (doc.payables_receivables === "Receivables") {
						child_table_field = "receivables";
						// Receivables → as is
					}

					if (doc.payables_receivables === "Payables") {
						child_table_field = "payables";
						// Payables → always positive
						amount = Math.abs(amount);
					}

					if (!child_table_field) {
						frappe.msgprint("Invalid Payables / Receivables value");
						return;
					}

					// 🔁 Duplicate check
					let already_exists = (frm.doc[child_table_field] || []).some(row => {
						return row.reference_document_type === doctype &&
							   row.reference_document === name;
					});

					if (already_exists) {
						frappe.msgprint("Notice Period Buyout already added");
						return;
					}

					// ➕ Add row
					let row = frm.add_child(child_table_field);
					row.reference_document_type = doctype;
					row.reference_document = name;
					row.amount = amount;
					row.component = "Notice Period Buyout";

					frm.refresh_field(child_table_field);

					frappe.show_alert({
						message: __("Notice Period Buyout added successfully"),
						indicator: "green"
					});
				}
			});
		});
	}
}