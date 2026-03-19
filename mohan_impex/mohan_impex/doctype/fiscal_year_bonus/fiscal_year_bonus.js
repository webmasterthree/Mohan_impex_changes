// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fiscal Year Bonus", {
    refresh: function(frm) {
        if (!frm.doc.docstatus){
            frm.add_custom_button("Get Employees", function() {

                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Employee",
                        filters: {
                            status: "Active"
                        },
                        fields: ["name", "employee_name"],
                        limit_page_length: 1000   // 🔥 IMPORTANT
                    },
                    callback: function(r) {

                        if (r.message) {

                            frm.clear_table("employee_bonus_table");

                            r.message.forEach(emp => {
                                let row = frm.add_child("employee_bonus_table");
                                row.employee = emp.name;
                                row.employee_name = emp.employee_name;
                            });

                            frm.refresh_field("employee_bonus_table");
                        }
                    }
                });

            });
        }
        if (frm.doc.docstatus == 1){
            let btn = frm.add_custom_button("Process Bonus Slip", function() {
                frappe.call({
                    method: "mohan_impex.mohan_impex.doctype.fiscal_year_bonus.fiscal_year_bonus.process_bonus_slip",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: "Processing...",
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint("Bonus Processed Successfully");
                            frm.reload_doc();
                        }
                    }
                });
            });

            $(btn).css({
                "background-color": "black",
                "color": "white",
                "border-color": "black"
            });
        }
    }
});