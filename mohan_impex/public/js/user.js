// frappe.ui.form.on('User', {
//     after_save: function(frm) {
//         if (frm.doc.roles && Array.isArray(frm.doc.roles)) {
//             let user_roles = frm.doc.roles.map(role => role.role);
//             if (user_roles.includes("Supplier") && user_roles.length === 1) {
//                 frappe.msgprint(__('Supplier Role Created'));

//                 frappe.new_doc('User Permission', {
//                     user: frm.doc.name,
//                     allow: 'Supplier',
//                 });
//             }
//         }
//     }
// });
