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

        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(
                __('Labour Payment Entry'),
                () => make_labour_payment_invoice(frm),
                __('Create')
            );
        }
    },
    after_save(frm) {
        fetch_po_fields_and_set_on_pr(frm);
    }
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
        frappe.msgprint(__('Custom Total Labour Cost is zero. Please check before creating invoice.'));
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
