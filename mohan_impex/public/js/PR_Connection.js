// frappe.ui.form.on('Purchase Receipt', {
//     refresh: function(frm) {
//         if (frm.doc.name) {
//             frappe.call({
//                 method: "mohan_impex.PR_Connection.get_linked_purchase_order",  // API method path
//                 args: { purchase_receipt: frm.doc.name },
//                 callback: function(response) {
//                     if (response.message && typeof response.message === "string") {
//                         let purchase_order = response.message;
//                         console.log("Linked Purchase Order:", purchase_order);

//                         let custom_type = '';
//                         if (purchase_order.startsWith("IMP")) {
//                             custom_type = 'Import';
//                         } else if (purchase_order.startsWith("DOM")) {
//                             custom_type = 'Domestic';
//                         }

//                         frm.set_value('custom_type', custom_type);
//                         frm.refresh_field('custom_type');  // Ensure UI updates
//                     } else {
//                         console.warn("No linked Purchase Order found.");
//                     }
//                 }
//             });
//         }
//     }
// });



// frappe.ui.form.on('Purchase Receipt', {
//     refresh: function(frm) {
//         if (frm.doc.name) {
//             frappe.call({
//                 method: "mohan_impex.PR_Connection.get_linked_purchase_order",  // Updated API method path
//                 args: { purchase_receipt: frm.doc.name },
//                 callback: function(response) {
//                     if (response.message) {
//                         let purchase_order = response.message;
//                         console.log("Linked Purchase Order:", purchase_order);

//                         if (purchase_order.startsWith("IMP")) {
//                             frm.set_value('custom_type', 'Import'); 
//                         } else if (purchase_order.startsWith("DOM")) {
//                             frm.set_value('custom_type', 'Domestic');  
//                         } else {
//                             frm.set_value('custom_type', '');  
//                         }
//                     } else {
//                         console.log("No linked Purchase Order found.");
//                     }
//                 }
//             });
//         }
//     }
// });
