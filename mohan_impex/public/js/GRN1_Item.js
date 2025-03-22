frappe.ui.form.on('Purchase Receipt', {
    items_add: function(frm, cdt, cdn) {
        sync_custom_item_details(frm);
    },
    items_remove: function(frm, cdt, cdn) {
        sync_custom_item_details(frm);
    },
    refresh: function(frm) {
        sync_custom_item_details(frm);
    }
});

frappe.ui.form.on('Purchase Receipt Item', {
    qty: function(frm, cdt, cdn) {
        sync_custom_item_details(frm);
    },
    rejected_qty: function(frm, cdt, cdn) {
        sync_custom_item_details(frm);
    },
    rate: function(frm, cdt, cdn) {
        sync_custom_item_details(frm);
    },
    batch_no: function(frm, cdt, cdn) {
        sync_custom_item_details(frm);
    }
});

function sync_custom_item_details(frm) {
    // Clear existing rows
    frm.clear_table('custom_item_details');

    // Loop through each item in items table
    frm.doc.items.forEach(item => {
        let new_row = frm.add_child('custom_item_details');

        // Compute expected and received quantities
        let expected_qty = item.qty + item.rejected_qty;
        let received_qty = item.qty;

        // Map values
        new_row.item_code     = item.item_code;
        new_row.expected_qty  = expected_qty;
        new_row.received_qty  = received_qty;
        new_row.unit_price    = item.rate;
        new_row.batch         = item.batch_no;

        // Set condition based on quantity comparison
        if (expected_qty === received_qty) {
            new_row.condition = 'All okay';
        } else if (received_qty < expected_qty) {
            new_row.condition = 'Short';
        }
    });

    // Refresh the child table
    frm.refresh_field('custom_item_details');
}





// frappe.ui.form.on('Purchase Receipt', {
//     items_add: function(frm, cdt, cdn) {
//         sync_custom_item_details(frm);
//     },
//     items_remove: function(frm, cdt, cdn) {
//         sync_custom_item_details(frm);
//     },
//     refresh: function(frm) {
//         sync_custom_item_details(frm);
//     }
// });

// frappe.ui.form.on('Purchase Receipt Item', {
//     qty: function(frm, cdt, cdn) {
//         sync_custom_item_details(frm);
//     },
//     rejected_qty: function(frm, cdt, cdn) {
//         sync_custom_item_details(frm);
//     },
//     rate: function(frm, cdt, cdn) {
//         sync_custom_item_details(frm);
//     },
//     batch_no: function(frm, cdt, cdn) {
//         sync_custom_item_details(frm);
//     }
// });

// function sync_custom_item_details(frm) {
//     // Clear existing custom_item_details
//     frm.clear_table('custom_item_details');

//     // Map data from items table to custom_item_details
//     frm.doc.items.forEach(item => {
//         let new_row = frm.add_child('custom_item_details');
        
//         new_row.item_code      = item.item_code;
//         new_row.expected_qty   = item.qty + item.rejected_qty;
//         new_row.received_qty   = item.qty;
//         new_row.unit_price     = item.rate;
//         new_row.batch          = item.batch_no;
//     });

//     frm.refresh_field('custom_item_details');
// }
