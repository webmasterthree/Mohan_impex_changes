// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Trial Target", {
	refresh(frm) {
        set_comp_item_filter(frm)
	},
    async validate(frm){
        await update_trial_status(frm)
        // await validate_trial(frm)
    },
    async before_workflow_action(frm){
        console.log(frm.doc.workflow_state)
        // frappe.throw("kihgufdytsyd")
        await validate_trial(frm)
    },
    after_workflow_action(frm){
        // frappe.throw("kihgufdytsyd")
        update_trial_status(frm)
    },
    item_code(frm){
        set_target_template(frm)
    },
    competitor_brand(frm){
        set_comp_item_filter(frm, true)
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

function set_comp_item_filter(frm, reset=false){
    if(reset){
        frm.set_value("comp_item", "")
    }
    if (frm.doc.competitor_brand){
        frappe.call({
            method: "mohan_impex.api.get_competitor_items",
            args: {
                competitor: frm.doc.competitor_brand
            },
            callback: function(r){
                const comp_items = r.data.map(item => item.item_name);
                frm.fields_dict.comp_item.set_data(comp_items)
            }
        })
    }
    else{
        frm.fields_dict.comp_item.set_data([])
    }
}

async function validate_trial(frm){
    await frm.call("validate_trial").then(async(r) => {
        if (r.message) {
          frappe.throw(r.message)
        }
    });
}

async function update_trial_status(frm){
    await frm.call("update_trial_status").then(async(r) => {
        console.log(r.message)
        if (r.message) {
          frappe.throw(r.message)
        }
    });
}