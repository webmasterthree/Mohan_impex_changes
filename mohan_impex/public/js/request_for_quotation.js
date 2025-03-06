// frappe.ui.form.on("Request for Quotation Item", {
//     item_code: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn];

//         if (row.item_code) {
//             frappe.call({
//                 method: "mohan_impex.supplier_item.get_suppliers_by_item",
//                 args: {
//                     item_name: row.item_code
//                 },
//                 callback: function(response) {
//                     if (response.message && response.message.suppliers.length > 0) {
//                         let suppliers = response.message.suppliers;

//                         // Set options for the supplier field in "Request for Quotation Supplier" child table
//                         frm.fields_dict["suppliers"].grid.get_field("supplier").get_query = function() {
//                             return {
//                                 filters: [
//                                     ["Supplier", "name", "in", suppliers]
//                                 ]
//                             };
//                         };

//                         frappe.msgprint({
//                             title: __("Filtered Suppliers"),
//                             message: __("Only the following suppliers are available: " + suppliers.join(", ")),
//                             indicator: "blue"
//                         });
//                     } else {
//                         frappe.msgprint({
//                             title: __("No Suppliers Found"),
//                             message: __("No suppliers available for the selected item."),
//                             indicator: "red"
//                         });
//                     }
//                 }
//             });
//         }
//     }
// });


frappe.ui.form.on("Request for Quotation Item", {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.item_code) {
            frappe.call({
                method: "mohan_impex.supplier_item.get_suppliers_by_item",
                args: { item_name: row.item_code },
                callback: function(response) {
                    if (response.message && response.message.suppliers.length > 0) {
                        let suppliers = response.message.suppliers;

                        // Get existing suppliers
                        let existing_suppliers = frm.doc.suppliers.map(s => s.supplier);

                        if (frm.doc.suppliers.length === 1 && !frm.doc.suppliers[0].supplier) {
                            // If first row is empty, use it instead of adding a new row
                            frm.doc.suppliers = [];
                        }

                        // Add only new suppliers
                        suppliers.forEach(supplier => {
                            if (!existing_suppliers.includes(supplier)) {
                                let child = frm.add_child("suppliers");
                                child.supplier = supplier;
                            }
                        });

                        frm.refresh_field("suppliers");
                    }
                }
            });
        }
    }
});
