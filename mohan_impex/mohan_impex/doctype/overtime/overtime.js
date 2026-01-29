// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime', {
    refresh: function(frm) {
        if(frappe.session.user != 'Administrator'){
            frm.set_df_property('bank_guarantee_table', 'cannot_add_rows', true);
            frm.set_df_property('bank_guarantee_table', 'cannot_delete_rows', true);
            // frm.disable_save();
        }
        // Calculate total overtime hours when form loads
        // calculate_total_overtime(frm);
    },
    onload: function(frm){
        // Example: Get the 'default_currency' from 'System Settings'
        frappe.db.get_single_value('Mohan Impex Settings', 'overtime_prhrs_rate')
            .then(value => {
                frm.set_value("overtime_prhrs_rate",value)
        });
    },
    validate: function(frm, cdt, cdn) {
        calculate_total_overtime(frm);
    }
});


frappe.ui.form.on('Overtime Table', {
    overtime_status: function(frm, cdt, cdn) {
        calculate_total_overtime(frm);
        lock_overtime_row(frm, cdn);
    },
    form_render(frm, cdt, cdn) {
        lock_overtime_row(frm, cdn);
    }
});


function calculate_total_overtime(frm) {
    let ot_total_hours = 0;
    
    $.each(frm.doc.overtime_table || [], function(i, row) {
        if(row.overtime_status == "Approved"){
            ot_total_hours += flt(row.overtime_hours);
        } 
    });
    
    frm.set_value('total_overtime_hours', ot_total_hours);

    let ap_total_hours = 0;
    
    $.each(frm.doc.overtime_table || [], function(i, row) {
        if(row.overtime_status == "Approved"){
            ap_total_hours += flt(row.approved_hours);
        } 
    });
    
    frm.set_value('total_approved_hours', ap_total_hours);
    
    // Calculate total amount if rate is available
    // if(frm.doc.overtime_per_hours_rate && frm.doc.total_overtime_hours > 0) {
        let total_amount = frm.doc.total_approved_hours * frm.doc.overtime_prhrs_rate;
        frm.set_value('total_hours_amount', total_amount);
    // }
}


function lock_overtime_row(frm, cdn) {
    const row = locals['Overtime Table'][cdn];
    if (!row) return;

    const grid = frm.fields_dict.overtime_table.grid;
    const grid_row = grid.grid_rows_by_docname[cdn];
    if (!grid_row) return;

    const locked = row.overtime_status === "Approved";

    grid_row.toggle_editable('overtime_hours', !locked);
    grid_row.toggle_editable('attendance_date', !locked);
    grid_row.toggle_editable('approved_hours', !locked);
    grid_row.toggle_editable('overtime_status', !locked);
}