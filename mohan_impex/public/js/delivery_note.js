frappe.ui.form.on('Delivery Note', {
    // Run all logic before saving the form
    validate: function (frm) {
        update_pre_unloading_status(frm);
        calculate_labour_cost(frm);
    },

    // Recalculate labour cost when related fields are changed
    custom_labour_rate_per_ton: function (frm) {
        calculate_labour_cost(frm);
    },
    custom_total_weight: function (frm) {
        calculate_labour_cost(frm);
    },
    custom_no_of_labour: function (frm) {
        calculate_labour_cost(frm);
    },
    custom_labour_rate: function (frm) {
        calculate_labour_cost(frm);
    },
    onload: function (frm) {
        if (frm.doc.docstatus === 1 && frm.doc.custom_total_labour_cost!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_dn_labour_payment",
                args: {
                    dn_labour_payment: frm.doc.name
                },
                callback: function (r) {
                    if (r.message === false) {
                        frm.add_custom_button(
                            __('Labour Payment Entry'),
                            () => make_labour_payment_invoice(frm),
                            __('Create')
                        );
                    }
                }
            });
        }
        if (frm.doc.docstatus === 1 && frm.doc.total_misc_amount!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_dn_misc_payment",
                args: {
                    dn_misc_expense: frm.doc.name
                },
                callback: function (r) {
                    if (r.message === false) {
                        frm.add_custom_button(
                            __('Misc Payment Entry'),
                            () => make_misc_payment_entry(frm),
                            __('Create')
                        );
                    }
                }
            });
        }
        if (frm.doc.docstatus === 1 && frm.doc.transport_charges!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_dn_transporter_payment",
                args: {
                    dn_transporter_payment: frm.doc.name
                },
                callback: function (r) {
                    if (r.message === false) {
                        frm.add_custom_button(
                            __('Transporter Payment Entry'),
                            () => transporter_payment_entry(frm),
                            __('Create')
                        );
                    }
                }
            });
        }
    },
    miscellaneous_expenses_remove(frm, cdt, cdn) {
        update_total_misc_amount(frm);
    },
});

function update_pre_unloading_status(frm) {
    let total_weight = frm.doc.items.reduce((sum, item) => {
        let qty = flt(item.stock_qty);
        return sum + qty;
    }, 0);

    frm.set_value('custom_total_weight', total_weight);

    frm.refresh_fields(['custom_total_weight']);
}


// Calculates total labour cost with fallback logic
function calculate_labour_cost(frm) {
    let total_weight = flt(frm.doc.custom_total_weight || 0);
    let labour_rate = flt(frm.doc.custom_labour_rate || 0);
    let factor = flt(frm.doc.conversion_factor || 1);
    let additional_cost = flt(frm.doc.additional_cost || 0);

    // Primary new formula
    let total_cost = 0;

    if (total_weight && labour_rate) {
        total_cost = (total_weight * labour_rate) / factor + additional_cost;
    }

    // Fallback: if still zero, check labour count logic
    if (total_cost === 0) {
        let no_of_labour = flt(frm.doc.custom_no_of_labour || 0);
        let rate_per_ton = flt(frm.doc.custom_labour_rate_per_ton || 0);

        if (no_of_labour && rate_per_ton && total_weight) {
            total_cost = (no_of_labour * rate_per_ton * total_weight) / 1000;
        }
    }

    frm.set_value('custom_total_labour_cost', total_cost);
}




// Main function: create Purchase Invoice from Purchase Receipt
function make_labour_payment_invoice(frm) {
    frappe.model.with_doctype('Purchase Invoice', () => {
        const pi = frappe.model.get_new_doc('Purchase Invoice');

        set_invoice_header_from_pr(pi, frm.doc);
        add_labour_item_row(pi, frm.doc);

        frappe.set_route('Form', 'Purchase Invoice', pi.name);
    });
}


// Map header fields
function set_invoice_header_from_pr(pi, pr) {
    Object.assign(pi, {
        supplier: pr.contractors_name,
        dn_labour_payment: pr.name
    });
}

function add_labour_item_row(pi, pr) {
    const labour_cost = flt(pr.custom_total_labour_cost || 0);

    if (!labour_cost) {
        frappe.msgprint(__('Total Labour Cost is zero. Please check before creating invoice.'));
    }

    const row = frappe.model.add_child(pi, 'Purchase Invoice Item', 'items');

    Object.assign(row, {
        item_template: 'Service Item',
        item_code: 'LABOUR CHARGE',
        item_name: 'LABOUR CHARGE',
        uom: 'NOS',
        qty: 1,
        rate: labour_cost,
    });
}




function make_misc_payment_entry(frm) {
    frappe.call({
        method: "mohan_impex.misc_payment_entry.misc_dn_payment_entry",
        args: {
            name: frm.doc.name,
        },
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
                pi.dn_misc_expense = data.name;

                (data.miscellaneous_expenses || []).forEach(row => {
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
            : (amt_precision || 2);

    let total = 0;

    (frm.doc.miscellaneous_expenses || []).forEach((d) => {
        total += flt(d.amount) || 0;
    });

    frm.set_value("total_misc_amount", flt(total, precision_to_use));
    frm.refresh_field("total_misc_amount");
}



function transporter_payment_entry(frm) {
    if (!frm.doc.transporter) {
        frappe.msgprint(__('Please set Transporter before creating Transport Payment Invoice.'));
        return;
    }

    if (!frm.doc.custom_transport_charges) {
        frappe.msgprint(__('Transport Charges is zero or not set.'));
        return;
    }

    frappe.model.with_doctype('Purchase Invoice', () => {
        const pi = frappe.model.get_new_doc('Purchase Invoice');

        pi.supplier = frm.doc.transporter;
        pi.dn_transporter_payment = frm.doc.name;

        const row = frappe.model.add_child(pi, 'items');
        row.item_template = 'Service Item'
        row.item_code = 'Transport-Services';
        row.item_name = 'Transport-Services';
        row.description = `Transport charges for ${frm.doc.name}`;
        row.uom = 'NOS';
        row.qty = 1;
        row.rate = frm.doc.custom_transport_charges || 0;
        frappe.set_route('Form', 'Purchase Invoice', pi.name);
    });
}
