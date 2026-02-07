frappe.ui.form.on('Gratuity', {
    employee: function(frm) {
        if (!frm.doc.employee) return;

        frappe.db.get_value('Employee', frm.doc.employee, 'date_of_joining')
            .then(r => {
                if (r.message && r.message.date_of_joining) {
                    let doj = frappe.datetime.str_to_obj(r.message.date_of_joining);
                    let today = frappe.datetime.str_to_obj(frappe.datetime.get_today());

                    // Difference in years
                    let diff_ms = today - doj;
                    let diff_years = diff_ms / (1000 * 60 * 60 * 24 * 365);

                    let full_years = Math.floor(diff_years);
                    let decimal_part = diff_years - full_years;

                    let considered_years = full_years;
                    if (decimal_part > 0.6) {
                        considered_years = full_years + 1;
                    }

                    // Set value in field
                    frm.set_value("current_work_experience", considered_years);
                    
                } else {
                    frm.set_value("current_work_experience", 0);
                }
            });
    }
});
