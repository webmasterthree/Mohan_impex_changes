frappe.ui.form.on('Pre-Unloading Check', {
    purchase_order: function (frm) {
        if (frm.doc.purchase_order) {
            frappe.call({
                method: "mohan_impex.sales_process_api.get_purchase_order_items",
                args: {
                    purchase_order: frm.doc.purchase_order
                },
                callback: function (r) {
                    if (r.message.status === "success") {
                        frm.clear_table("items");

                        r.message.data.forEach(function (item) {
                            let row = frm.add_child("items");
                            row.item_code = item.item_code;
                            row.shelf_life_in_days = item.shelf_life_in_days || 0;
                            row.qty = item.qty || 0;
                            row.uom = item.uom || "";
                            row.rate = item.rate || 0;
                            row.qty_in_stock_uom = item.stock_qty || 0;
                        });

                        frm.refresh_field("items");
                        update_pre_unloading_status(frm);
                    } else {
                        frappe.msgprint(__('No items found for this Purchase Order.'));
                    }
                }
            });
        }
    },

    validate: function(frm) {
        update_pre_unloading_status(frm);
    }
});

frappe.ui.form.on('Pre-Unloading Check Item', {
    manufacturing_date: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.manufacturing_date && row.shelf_life_in_days) {
            let manufacturing_date = frappe.datetime.str_to_obj(row.manufacturing_date);
            let today_date = frappe.datetime.str_to_obj(frappe.datetime.now_date());

            let days_since_mfg = frappe.datetime.get_day_diff(today_date, manufacturing_date);
            let remaining_shelf_life = row.shelf_life_in_days - days_since_mfg;

            frappe.model.set_value(cdt, cdn, 'remaining_shelf_life', remaining_shelf_life);

            if (remaining_shelf_life > 0) {
                frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Approved');
            } else {
                frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Pending');

                frappe.msgprint({
                    title: __('Warning'),
                    message: __('This item has expired! Purchase Team Approval is required.'),
                    indicator: 'red'
                });
            }
        }

        update_pre_unloading_status(frm);
    }
});

function update_pre_unloading_status(frm) {
    let has_pending_approval = frm.doc.items.some(item => item.purchase_team_approval === "Pending");

    frm.set_value('status', has_pending_approval ? 'Pending' : 'Approved');

    // Sum of all qtys
    let total_qty = frm.doc.items.reduce((sum, item) => sum + (item.qty_in_stock_uom || 0), 0);
    frm.set_value('total_quantity', total_qty);

    frm.refresh_fields(['status', 'total_quantity']);
}

// frappe.ui.form.on('Pre-Unloading Check', {
//     purchase_order: function (frm) {
//         if (frm.doc.purchase_order) {
//             frappe.call({
//                 method: "mohan_impex.sales_process_api.get_purchase_order_items",
//                 args: {
//                     purchase_order: frm.doc.purchase_order
//                 },
//                 callback: function (r) {
//                     if (r.message.status === "success") {
//                         frm.clear_table("items");

//                         r.message.data.forEach(function (item) {
//                             let row = frm.add_child("items");
//                             row.item_code = item.item_code;
//                             row.shelf_life_in_days = item.shelf_life_in_days || 0;
//                             row.qty = item.qty || 0;
//                             row.uom = item.uom || "";
//                             row.rate = item.rate || 0;
//                         });

//                         frm.refresh_field("items");
//                         update_pre_unloading_status(frm);
//                     } else {
//                         frappe.msgprint(__('No items found for this Purchase Order.'));
//                     }
//                 }
//             });
//         }
//     },

//     validate: function(frm) {
//         update_pre_unloading_status(frm);
//     }
// });

// frappe.ui.form.on('Pre-Unloading Check Item', {
//     manufacturing_date: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];

//         if (row.manufacturing_date && row.shelf_life_in_days) {
//             let manufacturing_date = frappe.datetime.str_to_obj(row.manufacturing_date);
//             let today_date = frappe.datetime.str_to_obj(frappe.datetime.now_date());

//             let days_since_mfg = frappe.datetime.get_day_diff(today_date, manufacturing_date);
//             let remaining_shelf_life = row.shelf_life_in_days - days_since_mfg;

//             frappe.model.set_value(cdt, cdn, 'remaining_shelf_life', remaining_shelf_life);

//             if (remaining_shelf_life > 0) {
//                 frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Approved');
//             } else {
//                 frappe.model.set_value(cdt, cdn, 'purchase_team_approval', 'Pending');

//                 frappe.msgprint({
//                     title: __('Warning'),
//                     message: __('This item has expired! Purchase Team Approval is required.'),
//                     indicator: 'red'
//                 });
//             }
//         }

//         update_pre_unloading_status(frm);
//     }
// });

// function update_pre_unloading_status(frm) {
//     let has_pending_approval = frm.doc.items.some(item => item.purchase_team_approval === "Pending");

//     frm.set_value('status', has_pending_approval ? 'Pending' : 'Approved');
//     frm.refresh_field('status');
// }

