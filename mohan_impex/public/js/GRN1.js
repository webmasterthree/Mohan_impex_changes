frappe.ui.form.on('Purchase Receipt', {
    // Run all logic before saving the form
    validate: function(frm) {
        update_pre_unloading_status(frm);
        calculate_labour_cost(frm);
    },

    // Recalculate labour cost when related fields are changed
    custom_labour_rate_per_ton: function(frm) {
        calculate_labour_cost(frm);
    },
    custom_total_weight: function(frm) {
        calculate_labour_cost(frm);
    },
    custom_no_of_labour: function(frm) {
        calculate_labour_cost(frm);
    },
    custom_labour_rate: function(frm) {
        calculate_labour_cost(frm);
    },
    onload: function(frm) {
        set_batch_query_filter(frm);
    }
});

frappe.ui.form.on('Purchase Receipt Item', {
    custom_manufacturing_date: function(frm, cdt, cdn) {
        calculate_remaining_shelf_life(frm, cdt, cdn);
    },

    custom_shelf_life_in_days: function(frm, cdt, cdn) {
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

// Updates overall purchase team approval status and total weight
function update_pre_unloading_status(frm) {
    let has_pending = frm.doc.items.some(item => item.custom_purchase_team_approval === "Pending");

    frm.set_value('custom_purchase_team_approval_status', has_pending ? 'Pending' : 'Approved');

    // Calculate total weight: (qty + rejected_qty) * conversion_factor
    let total_weight = frm.doc.items.reduce((sum, item) => {
        let qty = flt(item.qty) + flt(item.rejected_qty);
        let factor = flt(item.conversion_factor || 1);
        return sum + (qty * factor);
    }, 0);

    frm.set_value('custom_total_weight', total_weight);

    frm.refresh_fields(['custom_purchase_team_approval_status', 'custom_total_weight']);
}

// Calculates total labour cost with fallback logic
function calculate_labour_cost(frm) {
    let total_cost = 0;

    let rate_per_ton = flt(frm.doc.custom_labour_rate_per_ton || 0);
    let total_weight = flt(frm.doc.custom_total_weight || 0);

    // Primary calculation
    if (rate_per_ton && total_weight) {
        total_cost = (rate_per_ton * total_weight) / 1000;
    }

    // Fallback if total_cost is still zero
    if (total_cost === 0) {
        let no_of_labour = flt(frm.doc.custom_no_of_labour || 0);
        let labour_rate = flt(frm.doc.custom_labour_rate || 0);
        total_cost = (no_of_labour * labour_rate * total_weight) / 1000;
    }

    frm.set_value('custom_total_labour_cost', total_cost);
}
function set_batch_query_filter(frm) {
    frm.fields_dict.items.grid.get_field('batch_no').get_query = function(doc, cdt, cdn) {
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

