// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Notice Period Buyout", {
    onload:function(frm) {
        frm.set_query("salary_withholding", function() {
            return {
                "filters": {
                    "employee": frm.doc.employee,
                }
            };
        });
    },

    employee: function(frm){
        frappe.db.get_value('Salary Structure Assignment', {'employee': frm.doc.employee}, 'base')
            .then(r => {
                let base = r.message.base || 0;
                frm.set_value('base', base);
            });
        
        frappe.db.get_value('Salary Withholding', {'employee': frm.doc.employee}, 'name')
            .then(r => {
                let sw_name = r.message.name || 0;
                frm.set_value('salary_withholding', sw_name);
            });

        frappe.db.get_value('Leave Encashment', {'employee': frm.doc.employee}, 'name')
            .then(r => {
                let name = r.message.name;
                frm.set_value('leave_encashment', name);
            });

        if (!frm.doc.employee) {
            frm.clear_table("notice_period_buyout_table");
            frm.refresh_field("notice_period_buyout_table");
            frm.set_value("amount", 0);
            return;
        }

        add_withheld_salary_slips(frm);
    },

    refresh: function (frm) {
        frm.set_df_property('notice_period_buyout_table', 'cannot_add_rows', true);
        frm.set_df_property('notice_period_buyout_table', 'cannot_delete_rows', true);
    },
    salary_withholding: function(frm){
        if (!frm.doc.salary_withholding) {
            frm.set_value("amount", 0);
            return;
        }

        frappe.db.get_value(
            "Salary Withholding",
            frm.doc.salary_withholding,
            "number_of_withholding_cycles"
        ).then(r => {
            let cycles = r.message.number_of_withholding_cycles || 0;

            let slip_count = (frm.doc.notice_period_buyout_table || []).length;
            let base = frm.doc.base || 0;

            // Correct logic: remaining cycles
            let remaining_cycles = cycles - slip_count;

            if (remaining_cycles < 0) remaining_cycles = 0;

            let amount = remaining_cycles * base;

            frm.set_value("amount", amount - frm.doc.encashment_amount);
            if(frm.doc.amount > 0){
                frm.set_value("payables_receivables", 'Receivables');
            }else{
                frm.set_value("payables_receivables", 'Payables');
            }
        });
    }

});

function add_withheld_salary_slips(frm) {
    frm.clear_table("notice_period_buyout_table");
    frm.refresh_field("notice_period_buyout_table");

    frappe.db.get_list("Salary Slip", {
        filters: {
            employee: frm.doc.employee,
            status: "Withheld",
            docstatus: ["!=", 2]
        },
        fields: ["name"]
    }).then(r => {
        if (!r || !r.length) {
            frm.set_value("amount", 0);
            return;
        }

        r.forEach(slip => {
            let row = frm.add_child("notice_period_buyout_table");
            row.salary_slip = slip.name;
        });

        frm.refresh_field("notice_period_buyout_table");

        // agar salary_withholding pehle se selected hai → recalc
        if (frm.doc.salary_withholding) {
            frm.trigger("salary_withholding");
        }
    });
}
