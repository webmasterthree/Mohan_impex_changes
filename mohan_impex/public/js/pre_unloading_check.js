frappe.ui.form.on('Pre-Unloading Check', {
    purchase_order: function (frm) {
        if (frm.doc.purchase_order) {
            // Call the custom API to get Purchase Order Items with Shelf Life
            frappe.call({
                method: "mohan_impex.sales_process_api.get_purchase_order_items",
                args: {
                    purchase_order: frm.doc.purchase_order
                },
                callback: function (r) {
                    if (r.message.status === "success") {
                        frm.clear_table("items"); // Clear existing items

                        // Loop through API response and add item details to the child table
                        r.message.data.forEach(function (item) {
                            let row = frm.add_child("items");
                            row.item_code = item.item_code;
                            row.shelf_life_in_days = item.shelf_life_in_days || 0; // Set shelf life, default to 0 if undefined
                        });

                        frm.refresh_field("items"); // Refresh the child table
                        update_pre_unloading_status(frm); // Update status
                    } else {
                        frappe.msgprint(__('No items found for this Purchase Order.'));
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('Pre-Unloading Check Item', {
    manufacturing_date: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.manufacturing_date && row.shelf_life_in_days) {
            let manufacturing_date = frappe.datetime.str_to_obj(row.manufacturing_date);
            let today_date = frappe.datetime.str_to_obj(frappe.datetime.now_date());

            // Calculate Remaining Shelf Life
            let remaining_shelf_life = frappe.datetime.get_day_diff(today_date, manufacturing_date);
            remaining_shelf_life = Math.max(remaining_shelf_life, 0); // Ensure it's not negative
            
            // Set Remaining Shelf Life
            frappe.model.set_value(cdt, cdn, 'remaining_shelf_life', remaining_shelf_life);

            // Apply Approval Logic
            if (row.shelf_life_in_days < remaining_shelf_life) {
                frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Approved');
            } else {
                frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Pending');

                frappe.msgprint({
                    title: __('Warning'),
                    message: __('Remaining Shelf Life exceeds defined Shelf Life! Purchase Team Approval Required.'),
                    indicator: 'orange'
                });
            }
        }
        update_pre_unloading_status(frm);
    }
});

// Function to update the Pre-Unloading Check status based on item approvals
function update_pre_unloading_status(frm) {
    let has_pending_approval = frm.doc.items.some(item => item.purchase_team_approval === "Pending");

    frm.set_value('status', has_pending_approval ? 'Pending' : 'Approved');
    frm.refresh_field('status');
}


// frappe.ui.form.on('Pre-Unloading Check', {
//     purchase_order: function (frm) {
//         if (frm.doc.purchase_order) {
//             // Call the custom API to get Purchase Order Items with Shelf Life
//             frappe.call({
//                 method: "mohan_impex.sales_process_api.get_purchase_order_items",
//                 args: {
//                     purchase_order: frm.doc.purchase_order
//                 },
//                 callback: function (r) {
//                     if (r.message.status === "success") {
//                         frm.clear_table("items"); // Clear existing items

//                         // Loop through API response and add item details to the child table
//                         r.message.data.forEach(function (item) {
//                             let row = frm.add_child("items");
//                             row.item_code = item.item_code;
//                             row.shelf_life_in_days = item.shelf_life_in_days || 0; // Set shelf life, default to 0 if undefined
//                         });

//                         frm.refresh_field("items"); // Refresh the child table
//                         update_pre_unloading_status(frm); // Update status
//                     } else {
//                         frappe.msgprint(__('No items found for this Purchase Order.'));
//                     }
//                 }
//             });
//         }
//     }
// });

// frappe.ui.form.on('Pre-Unloading Check Item', {
//     manufacturing_date: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];

//         if (row.manufacturing_date && row.shelf_life_in_days) {
//             let manufacturing_date = frappe.datetime.str_to_obj(row.manufacturing_date);
//             let today = frappe.datetime.now_date();
//             let today_date = frappe.datetime.str_to_obj(today);

//             // Calculate expiry date
//             let expiry_date = frappe.datetime.add_days(manufacturing_date, row.shelf_life_in_days);
//             let remaining_shelf_life = frappe.datetime.get_day_diff(expiry_date, today_date);
//             remaining_shelf_life = Math.max(remaining_shelf_life, 0); // Ensure it's a positive value

//             // Set remaining shelf life field
//             frappe.model.set_value(cdt, cdn, 'remaining_shelf_life', remaining_shelf_life);

//             // Set purchase_team_approval based on shelf life
//             if (remaining_shelf_life < 30) {
//                 frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Pending'); // Requires approval
                
//                 frappe.msgprint({
//                     title: __('Warning'),
//                     message: __('Remaining Shelf Life is less than 30 days! Purchase Team Approval Required.'),
//                     indicator: 'orange'
//                 });

//             } else {
//                 frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Approved'); // Auto-approved if shelf life is okay
//             }
//         }
//         update_pre_unloading_status(frm);
//     }
// });

// // Function to update the Pre-Unloading Check status based on item approvals
// function update_pre_unloading_status(frm) {
//     let has_pending_approval = frm.doc.items.some(item => item.purchase_team_approval === "Pending");

//     if (has_pending_approval) {
//         frm.set_value('status', 'Pending');
//     } else {
//         frm.set_value('status', 'Approved');
//     }

//     frm.refresh_field('status');
// }
