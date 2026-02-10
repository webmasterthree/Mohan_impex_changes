frappe.ui.form.on('Purchase Receipt', {
    // Run all logic before saving the form
    validate: function (frm) {
        update_pre_unloading_status(frm);
        calculate_labour_cost(frm);
    },

    // Recalculate labour cost when related fields are changed
    custom_labour_rate_per_ton: function (frm) {
        calculate_labour_cost(frm);
    },
    custom_total_weight: function (frm) {
        calculate_labour_cost(frm);
    },
    custom_no_of_labour: function (frm) {
        calculate_labour_cost(frm);
    },
    custom_labour_rate: function (frm) {
        calculate_labour_cost(frm);
    },
    onload: function (frm) {
        set_batch_query_filter(frm);

        if (frm.doc.docstatus === 1 && frm.doc.custom_total_labour_cost!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_labour_payment",
                args: {
                    grn: frm.doc.name
                },
                callback: function (r) {
                    if (r.message === false) {
                        frm.add_custom_button(
                            __('Labour Payment Entry'),
                            () => make_labour_payment_invoice(frm),
                            __('Create')
                        );
                    }
                }
            });
        }
        if (frm.doc.docstatus === 1 && frm.doc.total_misc_amount!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_misc_payment",
                args: {
                    misc_expense: frm.doc.name
                },
                callback: function (r) {
                    if (r.message === false) {
                        frm.add_custom_button(
                            __('Misc Payment Entry'),
                            () => make_misc_payment_entry(frm),
                            __('Create')
                        );
                    }
                }
            });
        }
        if (frm.doc.docstatus === 1 && frm.doc.transport_charges!=0) {
            frappe.call({
                method: "mohan_impex.misc_payment_entry.has_transporter_payment",
                args: {
                    transporter_payment: frm.doc.name
                },
                callback: function (r) {
                    if (r.message === false) {
                        frm.add_custom_button(
                            __('Transporter Payment Entry'),
                            () => transporter_payment_entry(frm),
                            __('Create')
                        );
                    }
                }
            });
        }
    },
    after_save(frm) {
        fetch_po_fields_and_set_on_pr(frm);
    },
    miscellaneous_expenses_remove(frm, cdt, cdn) {
        update_total_misc_amount(frm);
    },
    // refresh(frm) {
        // if (frappe.session.user == "Administrator") {
        //     frm.add_custom_button("Check Expired Batches", function() {
        //         calculate_accept_reject(frm);
        //     });
        // }
        
        // if (frm.doc.workflow_state == "Purchase Team Approval Pending") {
        //     frm.page.clear_actions_menu();
        //     frm.page.set_primary_action('Review', () => {
        //         calculate_accept_reject1(frm);
        //     });
        // }
    // },
    refresh: async function(frm) {
        if (frappe.session.user == "Administrator") {
            frm.add_custom_button("Check Expired Batches", function() {
                calculate_accept_reject(frm);
            });
        }
        
        if (frm.doc.workflow_state == "Purchase Team Approval Pending") {
            frm.page.clear_actions_menu();
            frm.page.set_primary_action('Review', () => {
                calculate_accept_reject1(frm);
            });
        }
        // console.log("Complete button hidden due to shelf issue");
        let issue = await has_shelf_issue(frm);

        if (issue) {
            setTimeout(() => {
            // Replace 'ActionName' with the actual label of the button to hide
            frm.page.actions.find('[data-label="Complete"]').parent().parent().remove();
        }, 500);
            console.log("Complete button hidden due to shelf issue");
        }
    },
    
    before_workflow_action: async function(frm) {
        if (frm.doc.workflow_state === "Complete GRN") {
            
            // Check karo aur dialog dikhao agar zarurat ho
            await calculate_accept_reject(frm);
            
            // Agar dialog dikha hai (proceed = false), workflow ko rok do
            // if (proceed === false) {
            //     frappe.throw(__("Please review the expired/low shelf life items first"));
            // }
        }
    }
});

frappe.ui.form.on('Purchase Receipt Item', {
    custom_manufacturing_date: function (frm, cdt, cdn) {
        calculate_remaining_shelf_life(frm, cdt, cdn);
    },

    custom_shelf_life_in_days: function (frm, cdt, cdn) {
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


function update_pre_unloading_status(frm) {

    // Calculate total weight: (qty + rejected_qty) * conversion_factor
    let total_weight = frm.doc.items.reduce((sum, item) => {
        let qty = flt(item.qty) + flt(item.rejected_qty);
        let factor = flt(item.conversion_factor || 1);
        return sum + (qty * factor);
    }, 0);

    frm.set_value('custom_total_weight', total_weight);

    frm.refresh_fields(['custom_total_weight']);
}


// Calculates total labour cost with fallback logic
function calculate_labour_cost(frm) {
    let total_weight = flt(frm.doc.custom_total_weight || 0);
    let labour_rate = flt(frm.doc.custom_labour_rate || 0);
    let factor = flt(frm.doc.conversion_factor || 1);
    let additional_cost = flt(frm.doc.additional_cost || 0);

    // Primary new formula
    let total_cost = 0;

    if (total_weight && labour_rate) {
        total_cost = (total_weight * labour_rate) / factor + additional_cost;
    }

    // Fallback: if still zero, check labour count logic
    if (total_cost === 0) {
        let no_of_labour = flt(frm.doc.custom_no_of_labour || 0);
        let rate_per_ton = flt(frm.doc.custom_labour_rate_per_ton || 0);

        if (no_of_labour && rate_per_ton && total_weight) {
            total_cost = (no_of_labour * rate_per_ton * total_weight) / 1000;
        }
    }

    frm.set_value('custom_total_labour_cost', total_cost);
}



function set_batch_query_filter(frm) {
    frm.fields_dict.items.grid.get_field('batch_no').get_query = function (doc, cdt, cdn) {
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


// Main function: create Purchase Invoice from Purchase Receipt
function make_labour_payment_invoice(frm) {
    frappe.model.with_doctype('Purchase Invoice', () => {
        const pi = frappe.model.get_new_doc('Purchase Invoice');

        set_invoice_header_from_pr(pi, frm.doc);
        add_labour_item_row(pi, frm.doc);

        frappe.set_route('Form', 'Purchase Invoice', pi.name);
    });
}


// Map header fields
function set_invoice_header_from_pr(pi, pr) {
    Object.assign(pi, {
        supplier: pr.contractors_name,
        grn: pr.name
    });
}

function add_labour_item_row(pi, pr) {
    const labour_cost = flt(pr.custom_total_labour_cost || 0);

    if (!labour_cost) {
        frappe.msgprint(__('Total Labour Cost is zero. Please check before creating invoice.'));
    }

    const row = frappe.model.add_child(pi, 'Purchase Invoice Item', 'items');

    Object.assign(row, {
        item_template: 'Service Item',
        item_code: 'LABOUR CHARGE',
        item_name: 'LABOUR CHARGE',
        uom: 'NOS',
        qty: 1,
        rate: labour_cost,
    });
}


//=========== Fetch ASN Details From PO
function fetch_po_fields_and_set_on_pr(frm) {
    // Safety: if no items, nothing to do
    if (!frm.doc.items || frm.doc.items.length === 0) {
        return;
    }

    // Use first row's linked Purchase Order (optional guard)
    const po_in_item = frm.doc.items[0].purchase_order;
    if (!po_in_item) {
        return;
    }

    frappe.call({
        method: "mohan_impex.PR_Connection.get_linked_purchase_order",
        args: {
            purchase_receipt: frm.doc.name
        },
        callback: function (r) {
            if (!r.message) {
                return;
            }

            // If API returned an explicit error dict
            if (r.message.status === "error") {
                frappe.msgprint(
                    __("Error fetching Purchase Order details: {0}", [r.message.message])
                );
                return;
            }

            const data = r.message;

            frm.set_value("custom_transporters_name", data.custom_transporter_name || "");
            frm.set_value("custom_vehicle_no__container_no", data.custom_vehiclecontainer_number || "");
            frm.set_value("assigned_driver", data.custom_driver_name || "");
            frm.set_value("driver_mobile_number", data.custom_driver_mobile_number || "");
            frm.set_value("lr_number", data.lr_no || "");
        }
    });
}


function make_misc_payment_entry(frm) {
    frappe.call({
        method: "mohan_impex.misc_payment_entry.misc_payment_entry",
        args: {
            purchase_receipt: frm.doc.name,
        },
        callback: function (r) {
            const data = r.message;

            if (!data) {
                frappe.msgprint(__("No data returned from server."));
                return;
            }

            if (!data.miscellaneous_expenses || !data.miscellaneous_expenses.length) {
                frappe.msgprint(__("No Miscellaneous Expenses found to create Purchase Invoice."));
                return;
            }

            frappe.model.with_doctype("Purchase Invoice", () => {
                const pi = frappe.model.get_new_doc("Purchase Invoice");

                pi.supplier = data.misc_supplier;
                pi.misc_expense = data.name;

                (data.miscellaneous_expenses || []).forEach(row => {
                    const pi_item = frappe.model.add_child(pi, "items");

                    pi_item.item_template = row.misc_item_template;
                    pi_item.item_code = row.item_name;
                    pi_item.item_name = row.item_details;
                    pi_item.qty = row.qty;
                    pi_item.uom = row.uom;
                    pi_item.rate = row.rate || 0;
                    pi_item.amount = row.amount || 0;
                });

                frappe.set_route("Form", "Purchase Invoice", pi.name);
            });
        },
    });
}


frappe.ui.form.on("Miscellaneous Expense Items", {
    qty(frm, cdt, cdn) {
        update_item_amount_and_total(frm, cdt, cdn);
    },

    rate(frm, cdt, cdn) {
        update_item_amount_and_total(frm, cdt, cdn);
    },
});

function update_item_amount_and_total(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    const qty = flt(row.qty) || 0;
    const rate = flt(row.rate) || 0;
    const amt_precision = typeof precision === "function" ? precision("amount", row) : 2;

    const amount = flt(qty * rate, amt_precision);
    frappe.model.set_value(cdt, cdn, "amount", amount);

    update_total_misc_amount(frm, amt_precision);
}

function update_total_misc_amount(frm, amt_precision) {
    const precision_to_use =
        typeof precision === "function"
            ? precision("total_misc_amount", frm.doc)
            : (amt_precision || 2);

    let total = 0;

    (frm.doc.miscellaneous_expenses || []).forEach((d) => {
        total += flt(d.amount) || 0;
    });

    frm.set_value("total_misc_amount", flt(total, precision_to_use));
    frm.refresh_field("total_misc_amount");
}



function transporter_payment_entry(frm) {
    if (!frm.doc.transporter) {
        frappe.msgprint(__('Please set Transporter before creating Transport Payment Invoice.'));
        return;
    }

    if (!frm.doc.transport_charges) {
        frappe.msgprint(__('Transport Charges is zero or not set.'));
        return;
    }

    frappe.model.with_doctype('Purchase Invoice', () => {
        const pi = frappe.model.get_new_doc('Purchase Invoice');

        pi.supplier = frm.doc.transporter;
        pi.company = frm.doc.company;
        pi.transporter_payment = frm.doc.name;

        const row = frappe.model.add_child(pi, 'items');
        row.item_template = 'Service Item'
        row.item_code = 'Transport-Services';
        row.item_name = 'Transport-Services';
        row.description = `Transport charges for ${frm.doc.name}`;
        row.uom = 'NOS';
        row.qty = 1;
        row.rate = frm.doc.transport_charges || 0;
        frappe.set_route('Form', 'Purchase Invoice', pi.name);
    });
}



async function has_shelf_issue(frm) {

    const today = frappe.datetime.get_today();

    for (let item of frm.doc.items) {

        if (!item.serial_and_batch_bundle) continue;

        let rejected_qty = 0;
        let lt25_qty = 0;

        let sbb = await frappe.db.get_doc(
            "Serial and Batch Bundle",
            item.serial_and_batch_bundle
        );

        let shelf_days = sbb.custom_shelf_life_in_days || 0;

        for (let entry of sbb.entries) {

            if (!entry.batch_no || !entry.qty) continue;

            let batch = await frappe.db.get_value(
                "Batch",
                entry.batch_no,
                "expiry_date"
            );

            let expiry_date = batch.message.expiry_date;

            // Expired → Reject
            if (expiry_date && expiry_date < today) {
                rejected_qty += entry.qty;
                continue;
            }

            let remaining = entry.custom_remaining_shelf_life || 0;
            let percent = (shelf_days * remaining) / 100;

            if (percent < 25) {
                lt25_qty += entry.qty;
            }
        }

        // 🚨 Agar issue mila to turant true return
        if (rejected_qty > 0 || lt25_qty > 0) {
            return true;
        }
    }

    return false;
}






// ================= MAIN =================

async function calculate_accept_reject(frm) {

    const today = frappe.datetime.get_today();
    let dialog_data = [];
    let has_issue = false;

    for (let item of frm.doc.items) {

        if (!item.serial_and_batch_bundle) continue;

        let accepted_qty = 0;
        let rejected_qty = 0;
        let lt25_qty = 0;
        let gt25_qty = 0;

        let sbb = await frappe.db.get_doc(
            "Serial and Batch Bundle",
            item.serial_and_batch_bundle
        );

        let shelf_days = sbb.custom_shelf_life_in_days || 0;

        for (let entry of sbb.entries) {

            if (!entry.batch_no || !entry.qty) continue;

            let batch = await frappe.db.get_value(
                "Batch",
                entry.batch_no,
                "expiry_date"
            );

            let expiry_date = batch.message.expiry_date;

            if (expiry_date && expiry_date < today) {
                rejected_qty += entry.qty;
                continue;
            }

            accepted_qty += entry.qty;

            let remaining = entry.custom_remaining_shelf_life || 0;
            let percent = (shelf_days * remaining) / 100;

            if (percent < 25) lt25_qty += entry.qty;
            else gt25_qty += entry.qty;
        }

        dialog_data.push({
            item_code: item.item_code,
            lt25_qty,
            gt25_qty,
            accepted_qty,
            rejected_qty
        });

        if (rejected_qty > 0 || lt25_qty > 0) {
            has_issue = true;
        }
    }

    if (has_issue) {
        open_result_dialog(dialog_data, frm);
        return false;
    }

    return true;
}




// ================= DIALOG =================

async function open_result_dialog(data, frm) {

    let d = new frappe.ui.Dialog({
        title: "Review Items",
        size: "large",

        fields: [
            {
                fieldname: "items",
                fieldtype: "Table",
                cannot_add_rows: true,
                cannot_delete_rows: true,
                in_place_edit: false,
                data: data,
                fields: [
                    { fieldname:"item_code", fieldtype:"Data", label:"Item", in_list_view:1, read_only:1 },
                    { fieldname:"lt25_qty", fieldtype:"Float", label:"<25%", in_list_view:1, read_only:1 },
                    { fieldname:"gt25_qty", fieldtype:"Float", label:">25%", in_list_view:1, read_only:1 },
                    { fieldname:"accepted_qty", fieldtype:"Float", label:"Accepted", in_list_view:1, read_only:1 },
                    { fieldname:"rejected_qty", fieldtype:"Float", label:"Rejected", in_list_view:1, read_only:1 }
                ]
            }
        ],

        primary_action_label: "Send for Approval",

        primary_action: async function () {
            d.hide();

            try {
                // Directly update workflow state
                frm.set_value('workflow_state', 'Purchase Team Approval Pending');
                await frm.save();
                
                frappe.show_alert({
                    message: __("Sent for approval successfully"),
                    indicator: "green"
                });

            } catch (e) {
                console.error("Error:", e);
                frappe.msgprint({
                    title: __("Error"),
                    message: e.message,
                    indicator: "red"
                });
            }
        }
    });

    d.show();
    d.fields_dict.items.grid.refresh();
}

// // ✅ Client Script - YEH IMPORTANT HAI
// frappe.ui.form.on('Purchase Receipt', {
//     before_workflow_action: async function(frm) {
//         // Agar workflow state "Complete GRN" hai aur action "Send for Purchase Team Approval" hai
//         if (frm.doc.workflow_state === "Complete GRN" && 
//             frm.selected_workflow_action === "Send for Purchase Team Approval") {
            
//             // Check karo items mein issue hai ya nahi
//             let has_issue = await calculate_accept_reject(frm);
            
//             // ✅ Agar issue hai toh workflow ko PREVENT karo (return false)
//             if (has_issue) {
//                 frappe.validated = false; // Workflow ko rok do
//                 return false;
//             }
//         }
//     }
// });

// ✅ Client Script mein yeh event add karo
// frappe.ui.form.on('Purchase Receipt', {
//     before_workflow_action: async function(frm) {
//         // Agar workflow state "Complete GRN" hai aur action "Send for Purchase Team Approval" hai
//         if (frm.doc.workflow_state === "Complete GRN" && 
//             frm.selected_workflow_action === "Send for Purchase Team Approval") {
            
//             // Check karo aur dialog dikhao agar zarurat ho
//             let proceed = await calculate_accept_reject(frm);
            
//             // Agar dialog dikha hai (proceed = false), workflow ko rok do
//             if (proceed === false) {
//                 frappe.throw(__("Please review the expired/low shelf life items first"));
//             }
//         }
//     }
// });



// ===== FOR APPROVAL WITH BATCH SPLITTING =====
// async function calculate_accept_reject1(frm) {
//     const today = frappe.datetime.get_today();
//     let dialog_data = [];
//     let has_expired_or_low_shelf = false;

//     for (let item of frm.doc.items) {
//         if (!item.serial_and_batch_bundle) continue;

//         let accepted_qty = 0;
//         let rejected_qty = 0;
//         let lt25_qty = 0;
//         let gt25_qty = 0;

//         let sbb = await frappe.db.get_doc(
//             "Serial and Batch Bundle",
//             item.serial_and_batch_bundle
//         );

//         let shelf_days = sbb.custom_shelf_life_in_days || 0;

//         for (let entry of sbb.entries) {
//             if (!entry.batch_no || !entry.qty) continue;

//             let batch = await frappe.db.get_value(
//                 "Batch",
//                 entry.batch_no,
//                 "expiry_date"
//             );

//             let expiry_date = batch.message.expiry_date;

//             if (expiry_date && expiry_date < today) {
//                 rejected_qty += entry.qty;
//                 continue;
//             }

//             accepted_qty += entry.qty;

//             let remaining = entry.custom_remaining_shelf_life || 0;
//             let percent = (shelf_days * remaining) / 100;

//             if (percent < 25) {
//                 lt25_qty += entry.qty;
//             } else {
//                 gt25_qty += entry.qty;
//             }
//         }

//         dialog_data.push({
//             item_code: item.item_code,
//             item_name: item.name,
//             lt25_qty: lt25_qty,
//             gt25_qty: gt25_qty,
//             accepted_qty: accepted_qty,
//             rejected_qty: rejected_qty
//         });

//         if (rejected_qty > 0 || lt25_qty > 0) {
//             has_expired_or_low_shelf = true;
//         }
//     }

//     if (has_expired_or_low_shelf) {
//         open_approval_dialog(dialog_data, frm);
//     } else {
//         frappe.msgprint({
//             message: __("No expired or low shelf life items found. Proceeding with workflow."),
//             indicator: "green"
//         });
//         await proceed_with_workflow(frm, 'Approve');
//     }
// }

// // Dialog for Approval
// function open_approval_dialog(data, frm) {
//     let d = new frappe.ui.Dialog({
//         title: "Accept / Reject Items (Expiry & Shelf Life Based)",
//         size: "large",
//         fields: [
//             {
//                 fieldname: "items",
//                 fieldtype: "Table",
//                 label: "Item Summary",
//                 cannot_add_rows: true,
//                 in_place_edit: false,
//                 fields: [
//                     {
//                         fieldname: "item_code",
//                         fieldtype: "Data",
//                         label: "Item",
//                         in_list_view: 1,
//                         read_only: 1
//                     },
//                     {
//                         fieldname: "lt25_qty",
//                         fieldtype: "Float",
//                         label: "Shelf Life < 25% QTY",
//                         in_list_view: 1,
//                         read_only: 1
//                     },
//                     {
//                         fieldname: "gt25_qty",
//                         fieldtype: "Float",
//                         label: "Shelf Life > 25% QTY",
//                         in_list_view: 1,
//                         read_only: 1
//                     },
//                     {
//                         fieldname: "accepted_qty",
//                         fieldtype: "Float",
//                         label: "Accepted Total Qty",
//                         in_list_view: 1,
//                         read_only: 1
//                     },
//                     {
//                         fieldname: "rejected_qty",
//                         fieldtype: "Float",
//                         label: "Rejected Qty",
//                         in_list_view: 1,
//                         read_only: 1
//                     }
//                 ]
//             },
//             {
//                 fieldname: "section_break",
//                 fieldtype: "Section Break"
//             },
//             {
//                 fieldname: "rejected_warehouse",
//                 fieldtype: "Link",
//                 label: "Rejected Warehouse",
//                 options: "Warehouse",
//                 reqd: 1,
//                 description: "Select warehouse for rejected items"
//             }
//         ],
        
//         primary_action_label: __('Approve'),
//         primary_action: async function() {
//             let values = d.get_values();
            
//             if (!values.rejected_warehouse) {
//                 frappe.msgprint({
//                     message: __("Please select Rejected Warehouse"),
//                     indicator: "red"
//                 });
//                 return;
//             }

//             d.hide();

//             frappe.show_alert({
//                 message: __("Processing Approval..."),
//                 indicator: "blue"
//             });

//             try {
//                 let result = await frappe.call({
//                     method: "mohan_impex.purchase_receipt.split_rejected_batches",
//                     args: {
//                         pr_name: frm.doc.name,
//                         rejected_warehouse: values.rejected_warehouse
//                     }
//                 });

//                 if (result.message) {
//                     await frm.reload_doc();
//                     await proceed_with_workflow(frm, 'Approve');

//                     frappe.show_alert({
//                         message: __("Approved and sent for completion!"),
//                         indicator: "green"
//                     });
//                 }

//             } catch (error) {
//                 frappe.msgprint({
//                     title: __("Error"),
//                     message: error.message || __("Failed to process"),
//                     indicator: "red"
//                 });
//             }
//         }
//     });

//     d.add_custom_action(__('Reject'), async function() {
//         frappe.confirm(
//             __('Are you sure you want to reject this Purchase Receipt?'),
//             async function() {
//                 d.hide();
                
//                 frappe.show_alert({
//                     message: __("Processing Rejection..."),
//                     indicator: "orange"
//                 });

//                 try {
//                     await proceed_with_workflow(frm, 'Reject');

//                     frappe.show_alert({
//                         message: __("Purchase Receipt Rejected!"),
//                         indicator: "red"
//                     });

//                 } catch (error) {
//                     frappe.msgprint({
//                         title: __("Error"),
//                         message: error.message || __("Failed to reject"),
//                         indicator: "red"
//                     });
//                 }
//             }
//         );
//     });

//     d.show();
//     d.fields_dict.items.df.data = data;
//     d.fields_dict.items.grid.refresh();
// }

// async function proceed_with_workflow(frm, action_type) {
//     if (frm.doc.docstatus === 0) {
//         await frm.save();
//     }
    
//     let workflow_action = '';
    
//     if (action_type === 'Approve') {
//         workflow_action = 'Complete GRN';
//     } else if (action_type === 'Reject') {
//         workflow_action = 'Rejected By Purchase Team';
//     }
    
//     if (workflow_action) {
//         await frappe.xcall('frappe.model.workflow.apply_workflow', {
//             doc: frm.doc,
//             action: workflow_action
//         });
//     }
    
//     await frm.reload_doc();
// }








async function calculate_accept_reject1(frm) {

const today = frappe.datetime.get_today();
let dialog_data = [];

for (let item of frm.doc.items) {

    if (!item.serial_and_batch_bundle) continue;

    let accepted_qty = 0;
    let rejected_qty = 0;

    let lt25_qty = 0;
    let gt25_qty = 0;

    // 1️⃣ Get Serial and Batch Bundle
    let sbb = await frappe.db.get_doc(
        "Serial and Batch Bundle",
        item.serial_and_batch_bundle
    );

    let shelf_days = sbb.custom_shelf_life_in_days || 0;

    // 2️⃣ Loop child table
    for (let entry of sbb.entries) {

        if (!entry.batch_no || !entry.qty) continue;

        // 3️⃣ Get Batch expiry date
        let batch = await frappe.db.get_value(
            "Batch",
            entry.batch_no,
            "expiry_date"
        );

        let expiry_date = batch.message.expiry_date;

        // 4️⃣ Expiry logic (Rejected untouched)
        if (expiry_date && expiry_date < today) {
            rejected_qty += entry.qty;
            continue;
        }

        // ✅ Accepted
        accepted_qty += entry.qty;

        // 5️⃣ Shelf life %
        let remaining = entry.custom_remaining_shelf_life || 0;
        let percent = (shelf_days * remaining) / 100;

        // 6️⃣ Split accepted qty
        if (percent < 25) {
            lt25_qty += entry.qty;
        } else {
            gt25_qty += entry.qty;
        }
    }

    // 7️⃣ Push item-wise result
    dialog_data.push({
        item_code: item.item_code,
        item_name: item.name,
        lt25_qty: lt25_qty,
        gt25_qty: gt25_qty,
        accepted_qty: accepted_qty,
        rejected_qty: rejected_qty
    });
}

open_result_dialog1(dialog_data, frm);

}

function open_result_dialog1(data, frm) {

let d = new frappe.ui.Dialog({
    title: "Accepted / Rejected Qty (Expiry Based)",
    size: "large",
    fields: [
        {
            fieldname: "rejected_warehouse",
            fieldtype: "Link",
            label: "Rejected Warehouse",
            options: "Warehouse",
            reqd: 1,
            description: "Select warehouse for rejected batches"
        },
        {
            fieldname: "section_break",
            fieldtype: "Section Break"
        },
        {
            fieldname: "items",
            fieldtype: "Table",
            label: "Item Summary",
            cannot_add_rows: true,
            in_place_edit: false,
            fields: [
                {
                    fieldname: "item_code",
                    fieldtype: "Data",
                    label: "Item",
                    in_list_view: 1,
                    read_only: 1
                },
                {
                    fieldname: "lt25_qty",
                    fieldtype: "Float",
                    label: "Shelf Life < 25% QTY",
                    in_list_view: 1,
                    read_only: 1
                },
                {
                    fieldname: "gt25_qty",
                    fieldtype: "Float",
                    label: "Shelf Life > 25% QTY",
                    in_list_view: 1,
                    read_only: 1
                },
                {
                    fieldname: "accepted_qty",
                    fieldtype: "Float",
                    label: "Accepted Total Qty",
                    in_list_view: 1,
                    read_only: 1
                },
                {
                    fieldname: "rejected_qty",
                    fieldtype: "Float",
                    label: "Rejected Qty",
                    in_list_view: 1,
                    read_only: 1
                }
            ]
        }
    ],

    primary_action_label: "Approve",
    primary_action: async function() {
        await process_split_batches(d, frm, "Approved");
    },
    
    secondary_action_label: "Reject",
    secondary_action: async function() {
        await process_split_batches(d, frm, "Rejected");
    }
});

d.show();

// Set table data
d.fields_dict.items.df.data = data;
d.fields_dict.items.grid.refresh();

}

async function process_split_batches(dialog, frm, workflow_status) {
    
    let values = dialog.get_values();
    
    // ✅ Validate warehouse selection
    if (!values.rejected_warehouse) {
        frappe.msgprint({
            title: __("Required"),
            message: __("Please select Rejected Warehouse"),
            indicator: "red"
        });
        return;
    }

    dialog.hide();

    frappe.show_alert({
        message: __("Processing..."),
        indicator: "blue"
    });

    try {
        let result = await frappe.call({
            method: "mohan_impex.purchase_receipt.split_rejected_batches",
            args: {
                pr_name: frm.doc.name,
                rejected_warehouse: values.rejected_warehouse,
                workflow_status: workflow_status
            }
        });

        if (result.message) {
            for (let item_name in result.message) {

                let item_row = frm.doc.items.find(
                    i => i.name === item_name
                );

                if (item_row) {
                    frappe.model.set_value(
                        item_row.doctype,
                        item_row.name,
                        "rejected_serial_and_batch_bundle",
                        result.message[item_name].rejected_bundle
                    );
                    
                    // Update rejected warehouse
                    frappe.model.set_value(
                        item_row.doctype,
                        item_row.name,
                        "rejected_warehouse",
                        result.message[item_name].rejected_warehouse
                    );
                }
            }

            // ✅ Update workflow status
            if (result.message.workflow_status) {
                frm.set_value("workflow_state", result.message.workflow_status);
            }

            frm.refresh_field("items");

            frappe.show_alert({
                message: __(workflow_status === "Approved" ? 
                    "Approved successfully!" : 
                    "Rejected successfully!"),
                indicator: workflow_status === "Approved" ? "green" : "orange"
            });
            
            // Reload form to reflect workflow changes
            frm.reload_doc();
        }

    } catch (error) {
        frappe.msgprint({
            title: __("Error"),
            message: error.message || __("Failed to process"),
            indicator: "red"
        });
    }
}