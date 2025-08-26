frappe.ui.form.on('Serial and Batch Bundle', {
    onload(frm) {
        if (frm.doc.entries && frm.doc.entries.length) {
            recompute_all_entries(frm);
            update_pre_unloading_status(frm);
        }
    },

    validate(frm) {
        recompute_all_entries(frm);
        update_pre_unloading_status(frm);
    },

    // If parent shelf-life changes, recompute all rows
    custom_shelf_life_in_days(frm) {
        recompute_all_entries(frm);
        update_pre_unloading_status(frm);
    }
});

frappe.ui.form.on('Serial and Batch Entry', {
    custom_manufacturing_date(frm, cdt, cdn) {
        calculate_remaining_shelf_life(frm, cdt, cdn, { show_alert: true });
        update_pre_unloading_status(frm);
    },

    entries_add(frm) {
        recompute_all_entries(frm);
        update_pre_unloading_status(frm);
    },

    entries_remove(frm) {
        recompute_all_entries(frm);
        update_pre_unloading_status(frm);
    }
});

// ───────────────────────────────
// Core calculators
// ───────────────────────────────
function calculate_remaining_shelf_life(frm, cdt, cdn, opts = {}) {
    const row = locals[cdt][cdn];
    const show_alert = !!opts.show_alert;
    const shelf_life_days = cint(frm.doc.custom_shelf_life_in_days);

    if (!shelf_life_days || !row.custom_manufacturing_date) {
        clear_row_fields(cdt, cdn);
        return;
    }

    const mfg_date = frappe.datetime.str_to_obj(row.custom_manufacturing_date);
    const today = frappe.datetime.str_to_obj(frappe.datetime.now_date());
    if (!mfg_date || !today) {
        clear_row_fields(cdt, cdn);
        return;
    }

    const days_since_mfg = frappe.datetime.get_day_diff(today, mfg_date);
    const remaining_life = Math.max(0, shelf_life_days - days_since_mfg);

    frappe.model.set_value(cdt, cdn, 'custom_remaining_shelf_life', remaining_life);

    if (remaining_life > 0) {
        frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', 'Approved');
    } else {
        frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', 'Pending');
        if (show_alert) {
            frappe.msgprint({
                title: __('Warning'),
                message: __('This entry has expired! Purchase Team Approval is required.'),
                indicator: 'red'
            });
        }
    }
}

function recompute_all_entries(frm) {
    if (!Array.isArray(frm.doc.entries)) return;
    frm.doc.entries.forEach(d => {
        calculate_remaining_shelf_life(frm, d.doctype, d.name, { show_alert: false });
    });
}

function update_pre_unloading_status(frm) {
    const has_pending = (frm.doc.entries || []).some(
        it => it.custom_purchase_team_approval === 'Pending'
    );
    frm.set_value('custom_purchase_team_approval_status', has_pending ? 'Pending' : 'Approved');
    frm.refresh_field('custom_purchase_team_approval_status');
}

// Helpers
function clear_row_fields(cdt, cdn) {
    frappe.model.set_value(cdt, cdn, 'custom_remaining_shelf_life', null);
    frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', null);
}
function cint(val) {
    const n = parseInt(val, 10);
    return isNaN(n) ? 0 : n;
}
