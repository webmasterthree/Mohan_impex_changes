// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Segment", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Base Product", {
    base_products_add(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.product_name = frm.doc.base_product;
        row.uom = frm.doc.base_product_uom;
        frm.refresh_field("base_products");
    }
});