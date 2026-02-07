frappe.ui.form.on('Batch', {
    manufacturing_date: function (frm) {
        fatch_days(frm)
    },
    item: function(frm) {
        fatch_days(frm)
    }
});


function fatch_days(frm){
    if (!frm.doc.item || !frm.doc.manufacturing_date) return;

    frappe.db.get_value('Item', frm.doc.item, 'shelf_life_in_days')
        .then(r => {
            let shelf_life = r.message.shelf_life_in_days;
            if (!shelf_life) return;

            // manufacturing_date → Date object
            let mfg_date = frappe.datetime.str_to_obj(frm.doc.manufacturing_date);

            // add shelf life days
            let expiry_date = frappe.datetime.add_days(mfg_date, shelf_life);

            // set expiry_date
            frm.set_value(
                'expiry_date',
                frappe.datetime.obj_to_str(expiry_date)
            );
        });
}