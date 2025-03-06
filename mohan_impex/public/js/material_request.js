frappe.ui.form.on('Material Request Item', {
    item_code: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];

        // Clear the brand field if no item_code is selected
        if (!row.item_code) {
            frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
            return;
        }

        // Fetch item details based on item_code
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Item',
                name: row.item_code,
            },
            callback: function (response) {
                if (response.message) {
                    const itemData = response.message;

                    // Determine brand options
                    let brandOptions = '';
                    if (itemData.custom_select_brand && Array.isArray(itemData.custom_select_brand)) {
                        // If custom_select_brand exists and is an array, join the options
                        brandOptions = itemData.custom_select_brand
                            .map(obj => obj.brand_item)
                            .join('\n');
                    } else if (itemData.brand_name) {
                        // If a single brand name exists
                        brandOptions = itemData.brand_name;
                    }

                    // Update the brand field options or handle no brand options
                    if (brandOptions) {
                        // Update the options for the custom_select_brand field in the grid row
                        frm.fields_dict.items.grid.update_docfield_property('custom_select_brand', 'options', brandOptions);

                        // Optionally clear the current brand value to allow re-selection
                        frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
                    } else {
                        frappe.msgprint({
                            title: __('No Brand Options'),
                            message: __('No brand options available for the selected Item Code.'),
                            indicator: 'orange',
                        });
                        frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
                    }
                } else {
                    frappe.msgprint({
                        title: __('Item Not Found'),
                        message: __('Item details not found for the given Item Code.'),
                        indicator: 'red',
                    });
                    frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
                }
            },
            error: function () {
                frappe.msgprint({
                    title: __('Error'),
                    message: __('Unable to fetch Item details. Please try again later.'),
                    indicator: 'red',
                });
                frappe.model.set_value(cdt, cdn, 'custom_select_brand', '');
            },
        });
    },
});
