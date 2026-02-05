frappe.ui.form.on('Leave Encashment', {
    refresh(frm) {

        // Employee select nahi hua ho to call mat karo
        if (!frm.doc.employee) return;

        frappe.call({
            method: "mohan_impex.leave_encashment.get_formula",
            args: {
                emp: frm.doc.employee
            },
            freeze: true,
            callback(r) {

                if (r.message && r.message.length) {
                    const formula = r.message[0].custom_formula;
                    frm.set_value("custom_formula", formula);
                }
            }
        });
    }
});
