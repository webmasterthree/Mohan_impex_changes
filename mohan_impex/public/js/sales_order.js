frappe.ui.form.on("Sales Order", {
    refresh: function (frm) {
        console.log("✅ Client script loaded successfully!");

        // Ensure the button only binds the event once
        if (frm.fields_dict.custom_add_items_from_item_template) {
            frm.fields_dict.custom_add_items_from_item_template.$wrapper.on('click', function () {
                console.log("🛠 Custom Button Clicked! Running `show_item_selection_dialog` function...");
                show_item_selection_dialog(frm);
            });
        }
    }
});

function show_item_selection_dialog(frm) {
    let d = new frappe.ui.Dialog({
        title: __("Select Item"),
        fields: [
            {
                label: __("Item"),
                fieldname: "item_code",
                fieldtype: "Link",
                options: "Item",
                reqd: 1,
                get_query: function () {
                    return {
                        filters: {
                            "has_variants": 1  // ✅ This ensures only template items show up
                        }
                    };
                }
            }
        ],
        primary_action_label: __("Find Similar Items"),
        primary_action(values) {
            if (!values.item_code) {
                frappe.msgprint(__("Please select an item."));
                return;
            }

            console.log("🔍 Fetching attributes for item:", values.item_code);

            frappe.call({
                method: "mohan_impex.item_template.get_item_attributes",
                args: { item_code: values.item_code },
                callback: function (r) {
                    if (r.message && r.message.attributes.length > 0) {
                        d.hide();
                        console.log("✅ Attributes retrieved:", r.message.attributes);
                        show_attribute_selection_dialog(frm, values.item_code, r.message.attributes);
                    } else {
                        frappe.msgprint(__("No attributes found for this item."));
                    }
                }
            });
        }
    });

    d.show();
}

function show_attribute_selection_dialog(frm, item_code, attributes) {
    function slugify(text) {
        return text.toLowerCase().replace(/\s+/g, "_").replace(/[^a-z0-9_]/g, "");
    }

    let fields = attributes.map(attr => ({
        label: attr.attribute,
        fieldname: slugify(attr.attribute),
        fieldtype: "MultiCheck",
        options: attr.values.map(val => ({
            label: val.attribute_value,
            value: val.attribute_value
        }))
    }));

    let d = new frappe.ui.Dialog({
        title: __("Select Attributes to Match"),
        fields: fields,
        primary_action_label: __("Search Items"),
        primary_action(values) {
            console.log("🎯 Selected Attributes:", values);
            d.hide();
            search_matching_items(frm, item_code, values);
        }
    });

    d.show();
}

function search_matching_items(frm, selected_item, selected_attributes) {
    console.log("🔎 Searching for items matching:", selected_attributes);

    frappe.call({
        method: "mohan_impex.item_template.get_matching_items",
        args: {
            selected_item: selected_item,
            selected_attributes: JSON.stringify(selected_attributes)
        },
        callback: function (r) {
            if (r.message && r.message.length > 0) {
                console.log("✅ Matching items found:", r.message);
                show_matching_items_dialog(frm, r.message);
            } else {
                frappe.msgprint(__("No matching items found for the selected attributes."));
            }
        }
    });
}

function show_matching_items_dialog(frm, matching_items) {
    let d = new frappe.ui.Dialog({
        title: __("Select a Matching Item"),
        fields: [
            {
                label: __("Matching Items"),
                fieldname: "selected_item",
                fieldtype: "Link",
                options: "Item",
                reqd: 1,
                get_query: function () {
                    return {
                        filters: { "item_code": ["in", matching_items.map(item => item.item_code)] }
                    };
                }
            }
        ],
        primary_action_label: __("Apply Item"),
        primary_action(values) {
            if (!values.selected_item) {
                frappe.msgprint(__("Please select a matching item."));
                return;
            }

            console.log("✅ Adding item to Sales Order table:", values.selected_item);

            // Add the selected item to the "items" table
            let child = frm.add_child("items");
            child.item_code = values.selected_item;

            frm.refresh_field("items"); // Refresh the items table to reflect changes
            d.hide();
        }
    });

    d.show();
}




