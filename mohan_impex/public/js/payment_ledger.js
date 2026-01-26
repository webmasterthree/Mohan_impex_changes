// frappe.ui.form.on("Payment Doc Type", {
// 	links_add(frm, cdt, cdn) {
// 		// always sync document_type from parent
// 		frappe.model.set_value(
// 			cdt,
// 			cdn,
// 			"document_type",
// 			frm.doc.payment_against || ""
// 		);

// 		const party_name = (frm.doc.supplier || "").trim();
// 		const payment_type = (frm.doc.service_payment_type || "").trim();

// 		// required inputs
// 		if (!party_name || !payment_type) {
// 			frappe.msgprint("Please select Supplier and Service Payment Type first.");
// 			return;
// 		}

// 		// decide API by payment_against
// 		let method = null;

// 		if (frm.doc.payment_against === "Purchase Receipt") {
// 			method = "mohan_impex.pr_invoice.pr_invoice";
// 		} else if (frm.doc.payment_against === "Delivery Note") {
// 			method = "mohan_impex.dn_invoice.dn_invoice";
// 		} else {
// 			// for other values, do nothing
// 			return;
// 		}

// 		frappe.call({
// 			method: method,
// 			args: {
// 				party_name: party_name,
// 				payment_type: payment_type
// 			},
// 			callback: function (r) {
// 				const data = r.message || [];

// 				if (!Array.isArray(data) || data.length === 0) {
// 					frappe.msgprint(
// 						`No records found for ${frm.doc.payment_against} / ${party_name} / ${payment_type}.`
// 					);
// 					return;
// 				}

// 				// fill current + auto-add remaining rows
// 				data.forEach((d, i) => {
// 					let target_row = (i === 0)
// 						? locals[cdt][cdn]
// 						: frm.add_child("links");

// 					target_row.document_type = frm.doc.payment_against;
// 					target_row.link_name = d.name;             // DN or PR name
// 					target_row.amount = flt(d.amount || 0);    // amount from API

// 					// ✅ new fields from API (as per your server output keys)
// 					target_row.date = d.date || null;                 // posting_date mapped as date
// 					target_row.rate = flt(d.rate || 0);              // labour: custom_labour_rate, else: amount
// 					target_row.party_name = d.party_name || "";      // PR: supplier_name, DN: customer_name
// 				});

// 				frm.refresh_field("links");
// 			}
// 		});
// 	}
// });




frappe.ui.form.on("Payment Doc Type", {
	links_add(frm, cdt, cdn) {
		// always sync document_type from parent
		frappe.model.set_value(
			cdt,
			cdn,
			"document_type",
			frm.doc.payment_against || ""
		);

		const party_name = (frm.doc.supplier || "").trim();
		const payment_type = (frm.doc.service_payment_type || "").trim();

		const start_date = frm.doc.start_date || null;
		const end_date = frm.doc.end_date || null;

		if (!party_name || !payment_type) {
			frappe.msgprint("Please select Supplier and Service Payment Type first.");
			return;
		}

		if ((start_date && !end_date) || (!start_date && end_date)) {
			frappe.msgprint("Please select both Start Date and End Date.");
			return;
		}

		let method = null;
		if (frm.doc.payment_against === "Purchase Receipt") {
			method = "mohan_impex.pr_invoice.pr_invoice";
		} else if (frm.doc.payment_against === "Delivery Note") {
			method = "mohan_impex.dn_invoice.dn_invoice";
		} else {
			return;
		}

		frappe.call({
			method,
			args: {
				party_name,
				payment_type,
				from_date: start_date,
				to_date: end_date,
			},
			callback: function (r) {
				const data = r.message || [];

				if (!Array.isArray(data) || data.length === 0) {
					frappe.msgprint(
						`No records found for ${frm.doc.payment_against} / ${party_name} / ${payment_type}.`
					);
					return;
				}

				data.forEach((d, i) => {
					let target_row = (i === 0)
						? locals[cdt][cdn]
						: frm.add_child("links");

					target_row.document_type = frm.doc.payment_against;
					target_row.link_name = d.name;          // DN/PR name

					// numeric fields: let Frappe handle type coercion
					target_row.amount = d.amount ?? 0;
					target_row.rate = d.rate ?? 0;
					target_row.total_qty = d.total_qty ?? 0;

					// other fields
					target_row.date = d.date || null;       // posting_date
					target_row.party_name = d.party_name || "";
				});

				frm.refresh_field("links");
			}
		});
	}
});
