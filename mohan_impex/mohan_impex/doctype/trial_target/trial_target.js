// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Trial Target", {
	refresh(frm) {

	},
    item_code(frm){
        set_target_template(frm)
    }
});

function set_target_template(frm){
    if(frm.doc.item_code){
        frappe.call({
            method: "mohan_impex.mohan_impex.doctype.trial_target.trial_target.get_item_trial_template",
            args: {
                item_code: frm.doc.item_code
            },
            callback: function(r){
                frm.set_value("trial_target_table", r.message)
            }
        })
    }
    else{
        frm.set_value("trial_target_table", [])
    }
}