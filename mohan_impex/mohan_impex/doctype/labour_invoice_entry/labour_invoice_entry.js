// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Labour Invoice Entry", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Labour Detail', {
    no_of_labour: calculate_total,
    rate: calculate_total,
    overtime_hours: calculate_total,
    overtime_rate: calculate_total
});

function calculate_total(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    let normal = (row.no_of_labour || 0) * (row.rate || 0);
    let ot = (row.overtime_hours || 0) * (row.overtime_rate || 0);

    row.total = normal + ot;
    frm.refresh_field("labour_details");
}