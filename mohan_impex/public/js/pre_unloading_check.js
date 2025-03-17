frappe.ui.form.on('Pre-Unloading Check', {
    purchase_order: function (frm) {
        if (frm.doc.purchase_order) {
            // Call the custom API to get Purchase Order Items
            frappe.call({
                method: "mohan_impex.sales_process_api.get_purchase_order_items",
                args: {
                    purchase_order: frm.doc.purchase_order
                },
                callback: function (r) {
                    if (r.message.status === "success") {
                        frm.clear_table("items"); // Clear existing items

                        // Loop through API response and add item codes to the child table
                        r.message.data.forEach(function (item) {
                            let row = frm.add_child("items");
                            row.item_code = item.item_code; // Only setting item_code
                        });

                        frm.refresh_field("items"); // Refresh the child table
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

        if (row.manufacturing_date) {
            let manufacturing_date = frappe.datetime.str_to_obj(row.manufacturing_date);
            let today = frappe.datetime.now_date();
            let today_date = frappe.datetime.str_to_obj(today);

            // Calculate the remaining shelf life in days
            let remaining_shelf_life = frappe.datetime.get_day_diff(today_date, manufacturing_date);

            // Ensure it's a positive value
            remaining_shelf_life = Math.max(remaining_shelf_life, 0);

            // Set the calculated value in the field
            frappe.model.set_value(cdt, cdn, 'remaining_shelf_life', remaining_shelf_life);

            // Show a warning message if shelf life is below 30 days
            if (remaining_shelf_life < 30) {
                frappe.msgprint({
                    title: __('Warning'),
                    message: __('Remaining Shelf Life is less than 30 days!'),
                    indicator: 'orange'
                });
            }
        }
    }
});












// frappe.ui.form.on('Pre-Unloading Check Item', {
//     manufacturing_date: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];
        
//         if (row.manufacturing_date) {
//             let manufacturing_date = frappe.datetime.str_to_obj(row.manufacturing_date);
//             let today = frappe.datetime.now_date();
//             let today_date = frappe.datetime.str_to_obj(today);

//             // Calculate the remaining shelf life in days
//             let remaining_shelf_life = frappe.datetime.get_day_diff(today_date, manufacturing_date);

//             // Set the calculated value in the field
//             frappe.model.set_value(cdt, cdn, 'remaining_shelf_life', remaining_shelf_life);
//         }
//     }
// });
