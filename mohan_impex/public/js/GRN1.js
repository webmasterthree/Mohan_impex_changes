frappe.ui.form.on('Purchase Receipt', {
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
        set_batch_query_filter(frm);

        if (frm.doc.docstatus === 1 && frm.doc.custom_total_labour_cost!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_labour_payment",
                args: {
                    grn: frm.doc.name
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
                method: "mohan_impex.misc_payment_entry.has_misc_payment",
                args: {
                    misc_expense: frm.doc.name
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
                method: "mohan_impex.misc_payment_entry.has_transporter_payment",
                args: {
                    transporter_payment: frm.doc.name
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
    after_save(frm) {
        fetch_po_fields_and_set_on_pr(frm);
    },
    miscellaneous_expenses_remove(frm, cdt, cdn) {
        update_total_misc_amount(frm);
    },
});

frappe.ui.form.on('Purchase Receipt Item', {
    custom_manufacturing_date: function (frm, cdt, cdn) {
        calculate_remaining_shelf_life(frm, cdt, cdn);
    },

    custom_shelf_life_in_days: function (frm, cdt, cdn) {
        // Recalculate when shelf life is changed
        frappe.ui.form.trigger(cdt, cdn, 'custom_manufacturing_date');
    }
});

// Calculates remaining shelf life and sets purchase team approval status
function calculate_remaining_shelf_life(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    if (row.custom_manufacturing_date && row.custom_shelf_life_in_days) {
        let mfg_date = frappe.datetime.str_to_obj(row.custom_manufacturing_date);
        let today = frappe.datetime.str_to_obj(frappe.datetime.now_date());

        let days_since_mfg = frappe.datetime.get_day_diff(today, mfg_date);
        let remaining_life = row.custom_shelf_life_in_days - days_since_mfg;

        frappe.model.set_value(cdt, cdn, 'custom_remaining_shelf_life', remaining_life);

        if (remaining_life > 0) {
            frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', 'Approved');
        } else {
            frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', 'Pending');

            frappe.msgprint({
                title: __('Warning'),
                message: __('This item has expired! Purchase Team Approval is required.'),
                indicator: 'red'
            });
        }
    }

    update_pre_unloading_status(frm);
}


function update_pre_unloading_status(frm) {

    // Calculate total weight: (qty + rejected_qty) * conversion_factor
    let total_weight = frm.doc.items.reduce((sum, item) => {
        let qty = flt(item.qty) + flt(item.rejected_qty);
        let factor = flt(item.conversion_factor || 1);
        return sum + (qty * factor);
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



function set_batch_query_filter(frm) {
    frm.fields_dict.items.grid.get_field('batch_no').get_query = function (doc, cdt, cdn) {
        const row = locals[cdt][cdn];
        let filters = {
            item: row.item_code
        };

        if (row.custom_select_brand) {
            filters.custom_brand = row.custom_select_brand;
        }

        return { filters };
    };
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
        grn: pr.name
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


//=========== Fetch ASN Details From PO
function fetch_po_fields_and_set_on_pr(frm) {
    // Safety: if no items, nothing to do
    if (!frm.doc.items || frm.doc.items.length === 0) {
        return;
    }

    // Use first row's linked Purchase Order (optional guard)
    const po_in_item = frm.doc.items[0].purchase_order;
    if (!po_in_item) {
        return;
    }

    frappe.call({
        method: "mohan_impex.PR_Connection.get_linked_purchase_order",
        args: {
            purchase_receipt: frm.doc.name
        },
        callback: function (r) {
            if (!r.message) {
                return;
            }

            // If API returned an explicit error dict
            if (r.message.status === "error") {
                frappe.msgprint(
                    __("Error fetching Purchase Order details: {0}", [r.message.message])
                );
                return;
            }

            const data = r.message;

            frm.set_value("custom_transporters_name", data.custom_transporter_name || "");
            frm.set_value("custom_vehicle_no__container_no", data.custom_vehiclecontainer_number || "");
            frm.set_value("assigned_driver", data.custom_driver_name || "");
            frm.set_value("driver_mobile_number", data.custom_driver_mobile_number || "");
            frm.set_value("lr_number", data.lr_no || "");
        }
    });
}


function make_misc_payment_entry(frm) {
    frappe.call({
        method: "mohan_impex.misc_payment_entry.misc_payment_entry",
        args: {
            purchase_receipt: frm.doc.name,
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
                pi.misc_expense = data.name;

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

    if (!frm.doc.transport_charges) {
        frappe.msgprint(__('Transport Charges is zero or not set.'));
        return;
    }

    frappe.model.with_doctype('Purchase Invoice', () => {
        const pi = frappe.model.get_new_doc('Purchase Invoice');

        pi.supplier = frm.doc.transporter;
        pi.company = frm.doc.company;
        pi.transporter_payment = frm.doc.name;

        const row = frappe.model.add_child(pi, 'items');
        row.item_template = 'Service Item'
        row.item_code = 'Transport-Services';
        row.item_name = 'Transport-Services';
        row.description = `Transport charges for ${frm.doc.name}`;
        row.uom = 'NOS';
        row.qty = 1;
        row.rate = frm.doc.transport_charges || 0;
        frappe.set_route('Form', 'Purchase Invoice', pi.name);
    });
}
