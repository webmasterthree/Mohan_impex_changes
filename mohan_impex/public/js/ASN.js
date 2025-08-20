frappe.ui.form.on('Purchase Order', {
    refresh(frm) {
        // Always remove first to avoid duplicates
        frm.remove_custom_button('Create ASN');

        // Conditions to show ASN button
        if (
            frm.doc.custom_acceptance_status === "Accept" &&  // Supplier accepted
            frm.doc.total_qty !== frm.doc.custom_total_qtyasn && // Not fully ASN processed
            Array.isArray(frm.doc.items) && frm.doc.items.length > 0 // Has items
        ) {
            frm.add_custom_button(__('Create ASN'), () => {
                // Build ASN items from PO items
                const asn_items = frm.doc.items.map(row => ({
                    doctype: "ASN Item",
                    item: row.item_code,
                    qty: flt(row.qty) - flt(row.custom_asn_qty)
                }));

                // Compute parent total_qty
                const total_qty = asn_items.reduce((a, r) => a + flt(r.qty), 0);

                frappe.call({
                    method: "frappe.client.insert",
                    args: {
                        doc: {
                            doctype: "Advance Supplier Notification",
                            purchase_order: frm.doc.name,
                            supplier: frm.doc.supplier,
                            company: frm.doc.company,
                            items: asn_items,
                            total_qty: total_qty,
                            total_po_qty: frm.doc.total_qty // from PO
                        }
                    },
                    freeze: true,
                    freeze_message: __("Creating ASN..."),
                    callback(r) {
                        if (r.message) {
                            frappe.msgprint(
                                __('ASN {0} created. Total Qty: {1}', [r.message.name, total_qty])
                            );
                            frappe.set_route("Form", "Advance Supplier Notification", r.message.name);
                        }
                    }
                });
            });
        }
    }
});



// frappe.ui.form.on('Purchase Order', {
//     refresh(frm) {
//         // Avoid duplicate buttons on refresh
//         frm.remove_custom_button('Create ASN');

//         if (frm.doc.custom_acceptance_status === "Accept" && frm.doc.docstatus == 0) {
//             frm.add_custom_button('Create ASN', () => {
//                 if (!Array.isArray(frm.doc.items) || frm.doc.items.length === 0) {
//                     frappe.msgprint(__('No items found in this Purchase Order.'));
//                     return;
//                 }

//                 // Build ASN items from PO items
//                 const asn_items = frm.doc.items.map(row => ({
//                     doctype: "ASN Item",
//                     // NOTE: if your ASN child uses item_code, change "item" → "item_code"
//                     item: row.item_code,
//                     qty: flt(row.qty)
//                 }));

//                 // Compute parent total_qty
//                 const total_qty = asn_items.reduce((a, r) => a + flt(r.qty), 0);

//                 frappe.call({
//                     method: "frappe.client.insert",
//                     args: {
//                         doc: {
//                             doctype: "Advance Supplier Notification",
//                             purchase_order: frm.doc.name,
//                             supplier: frm.doc.supplier,
//                             company: frm.doc.company,
//                             items: asn_items,
//                             total_qty: total_qty,
//                             total_po_qty:total_qty
//                         }
//                     },
//                     freeze: true,
//                     freeze_message: __("Creating ASN..."),
//                     callback(r) {
//                         if (r.message) {
//                             frappe.msgprint(
//                                 __('ASN {0} created. Total Qty: {1}', [r.message.name, total_qty])
//                             );
//                             frappe.set_route("Form", "Advance Supplier Notification", r.message.name);
//                         }
//                     }
//                 });
//             });
//         }
//     }
// });



// // Helper to recalc total_qty from child rows
// function update_total_qty(frm) {
//     let total = 0;
//     (frm.doc.items || []).forEach(row => total += flt(row.qty));
//     frm.set_value("total_qty", total);
//     frm.refresh_field("total_qty");
// }

// // Parent Doctype events
// frappe.ui.form.on('Advance Supplier Notification', {
//     onload(frm) { update_total_qty(frm); },
//     refresh(frm) { update_total_qty(frm); },
//     items_add(frm) { update_total_qty(frm); },
//     items_remove(frm) { update_total_qty(frm); }
// });

// // Child Doctype events
// frappe.ui.form.on('ASN Item', {
//     qty(frm, cdt, cdn) {
//         const row = locals[cdt][cdn];
//         if (flt(row.qty) < 0) {
//             frappe.msgprint(__("Quantity cannot be negative."));
//             frappe.model.set_value(cdt, cdn, "qty", 0);
//         }
//         update_total_qty(frm);
//     }
// });
