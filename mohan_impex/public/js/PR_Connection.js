frappe.ui.form.on('Purchase Receipt', {
    refresh(frm) {
    	set_item_code_filter(frm);
    	if (frm.is_new()) {
            fetch_linked_po_data(frm);
        }
	}
});

function set_item_code_filter(frm){
    frm.fields_dict["items"].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
        let row = locals[cdt][cdn];
        return {
            filters: [
                ["has_variants", "=", 0],
                ["is_sales_item", "=", 1],
                ["variant_of", "=", row.item_template]
            ]
        };
    };
}



frappe.ui.form.on('Purchase Receipt Item', {
    item_code: function (frm, cdt, cdn) {
        const row = frappe.model.get_doc(cdt, cdn);

        if (!row.item_code) {
            frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
            frm.fields_dict.items.grid.update_docfield_property('custom_select_brand', 'options', ['']);
            return;
        }

        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Item",
                name: row.item_code
            },
            callback: function (r) {
                if (!r.exc && r.message) {
                    const brand_table = r.message.custom_select_brand || [];
                    const brand_options = brand_table.map(d => d.brand_item);
                    frm.fields_dict.items.grid.update_docfield_property(
                        'custom_select_brand',
                        'options',
                        [''].concat(brand_options)
                    );
                    frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
                    frm.fields_dict.items.grid.refresh_row(row);
                }
            }
        });
    }
});




function fetch_linked_po_data(frm) {
    frappe.call({
        method: "mohan_impex.PR_Connection.get_linked_purchase_order",
        args: { purchase_receipt: frm.doc.name },
        callback: function (r) {
            const purchase_order = r.message || '';

            if (purchase_order) {
                set_po_related_fields(frm, purchase_order);
            }
        }
    });
}


function set_po_related_fields(frm, purchase_order) {
    frappe.db.get_value('Purchase Order', purchase_order,
        ['custom_transporter_name', 'custom_vehiclecontainer_number']
    ).then(({ message }) => {
        if (message) {
            if (message.custom_transporter_name) {
                frm.set_value('custom_transporters_name', message.custom_transporter_name);
            }
            if (message.custom_vehiclecontainer_number) {
                frm.set_value('custom_vehicle_no__container_no', message.custom_vehiclecontainer_number);
            }
        }
    });
}