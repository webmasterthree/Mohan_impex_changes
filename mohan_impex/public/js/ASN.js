frappe.ui.form.on('Purchase Order', {
    refresh(frm) {
        // Remove existing button (from Create group) to avoid duplicates
        frm.remove_custom_button(__('Create ASN'), __('Create'));

        // Conditions to show ASN button
        if (
            frm.doc.custom_acceptance_status === "Accept" &&  // Supplier accepted
            frm.doc.total_qty !== frm.doc.custom_total_qtyasn && // Not fully ASN processed
            Array.isArray(frm.doc.items) && frm.doc.items.length > 0 // Has items
        ) {
            // Add under "Create" dropdown
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
            }, __('Create')); // 👈 this puts it inside the "Create" menu
        }
    }
});











