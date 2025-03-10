// frappe.ui.form.on("Sales Order", {
//     refresh(frm) {
//         console.log("✅ Client script loaded successfully!");

//         if (frm.fields_dict.custom_add_items_from_item_template) {
//             frm.trigger("setup_custom_button");
//         }
//     },
//     setup_custom_button(frm) {
//         frm.fields_dict.custom_add_items_from_item_template.$wrapper.off("click").on("click", function () {
//             console.log("🛠 Custom Button Clicked! Running `show_item_selection_dialog`...");
//             show_item_selection_dialog(frm);
//         });
//     }
// });

// function show_item_selection_dialog(frm) {
//     let dialog = new frappe.ui.Dialog({
//         title: __("Select Item Template"),
//         fields: [
//             {
//                 label: __("Item Template"),
//                 fieldname: "item_code",
//                 fieldtype: "Link",
//                 options: "Item",
//                 reqd: 1,
//                 get_query() {
//                     return { filters: { has_variants: 1 } };
//                 }
//             }
//         ],
//         primary_action_label: __("Find Variants"),
//         primary_action(values) {
//             if (!values.item_code) {
//                 frappe.msgprint(__("Please select an item template."));
//                 return;
//             }

//             console.log("🔍 Fetching attributes for:", values.item_code);

//             frappe.call({
//                 method: "mohan_impex.item_attr.get_item_template_attributes",
//                 args: { item_code: values.item_code },
//                 callback(r) {
//                     if (r.message && Object.keys(r.message).length > 0) {
//                         dialog.hide();
//                         console.log("✅ Attributes retrieved:", r.message);
//                         show_attribute_selection_dialog(frm, values.item_code, r.message[values.item_code]);
//                     } else {
//                         frappe.msgprint(__("No attributes found for this item template."));
//                     }
//                 }
//             });
//         }
//     });

//     dialog.show();
// }

// function show_attribute_selection_dialog(frm, item_template, attributes) {
//     let slugify = text => text.toLowerCase().replace(/\s+/g, "_").replace(/[^a-z0-9_]/g, "");

//     let fields = [
//         {
//             label: __("Selected Item Template"),
//             fieldname: "selected_item_display",
//             fieldtype: "HTML",
//             options: `<div class="alert alert-info">📌 Selected: <b>${item_template}</b></div>`,
//         },
//         {
//             fieldname: "selected_items",
//             fieldtype: "Hidden"
//         }
//     ];

//     Object.keys(attributes).forEach(attr => {
//         fields.push({
//             label: attr,
//             fieldname: slugify(attr),
//             fieldtype: "MultiCheck",
//             options: attributes[attr].map(val => ({ label: val, value: val })),
//             onchange() {
//                 let values = dialog.get_values();
//                 console.log("🎯 Attributes Changed:", values);
//                 update_matching_variants(frm, item_template, values, dialog);
//             }
//         });
//     });

//     fields.push({
//         label: __("Matching Variants"),
//         fieldname: "matching_variants_display",
//         fieldtype: "HTML",
//         options: `<div id="matching-variants" class="alert alert-light">🔍 Select attributes to see matching variants...</div>`,
//     });

//     let dialog = new frappe.ui.Dialog({
//         title: __("Select Attributes to Match"),
//         fields: fields,
//         primary_action_label: __("Search Variants"),
//         primary_action(values) {
//             console.log("🎯 Final Selected Attributes:", values);
//             dialog.hide();
//             search_matching_variants(frm, item_template, values);
//         }
//     });

//     dialog.show();
// }

// function update_matching_variants(frm, item_template, selected_attributes, dialog) {
//     console.log("🔎 Updating Matching Variants for:", item_template, "with attributes:", selected_attributes);

//     frappe.call({
//         method: "mohan_impex.item_attr.get_matching_items",
//         args: {
//             selected_item: item_template,
//             selected_attributes: JSON.stringify(selected_attributes)
//         },
//         callback(r) {
//             let container = document.getElementById("matching-variants");
//             if (!container) return;

//             if (r.message && r.message.length > 0) {
//                 console.log("✅ Matching variants found:", r.message);

//                 let htmlContent = `
//                     <button id="select-all-variants" class="btn btn-primary btn-sm mb-2">✔ Select All</button>
//                     <ul class="list-unstyled">`;

//                 r.message.forEach(item => {
//                     htmlContent += `<li class="border-bottom py-1">
//                         <input type="checkbox" name="selected_variants" value="${item.item_code}"> 
//                         ${item.item_code} - ${item.item_name}
//                     </li>`;
//                 });

//                 htmlContent += `</ul>`;
//                 container.innerHTML = htmlContent;

//                 setup_variant_selection(dialog);
//             } else {
//                 container.innerHTML = `<div class="alert alert-warning">❌ No matching variants found.</div>`;
//             }
//         }
//     });
// }

// function setup_variant_selection(dialog) {
//     let checkboxes = document.querySelectorAll("input[name='selected_variants']");
//     let selectAllButton = document.getElementById("select-all-variants");

//     selectAllButton.addEventListener("click", function () {
//         let allChecked = Array.from(checkboxes).every(cb => cb.checked);
//         checkboxes.forEach(cb => cb.checked = !allChecked);
//         update_selected_variants(dialog);
//     });

//     checkboxes.forEach(checkbox => {
//         checkbox.addEventListener("change", function () {
//             update_selected_variants(dialog);
//         });
//     });
// }

// function update_selected_variants(dialog) {
//     let selectedItems = Array.from(document.querySelectorAll("input[name='selected_variants']:checked"))
//         .map(cb => cb.value);

//     dialog.set_value("selected_items", selectedItems.join(","));

//     console.log("🔹 Updated selected variants:", selectedItems);
// }

// function search_matching_variants(frm, selected_item, selected_attributes) {
//     console.log("🔎 Searching for variants matching:", selected_attributes);

//     frappe.call({
//         method: "mohan_impex.item_attr.get_matching_items",
//         args: {
//             selected_item: selected_item,
//             selected_attributes: JSON.stringify(selected_attributes)
//         },
//         callback(r) {
//             if (r.message && r.message.length > 0) {
//                 console.log("✅ Matching variants found:", r.message);
//                 show_matching_variants_dialog(frm, r.message);
//             } else {
//                 frappe.msgprint(__("No matching variants found for the selected attributes."));
//             }
//         }
//     });
// }

// function show_matching_variants_dialog(frm, matching_items) {
//     let dialog = new frappe.ui.Dialog({
//         title: __("Select Matching Variants"),
//         fields: [
//             {
//                 label: __("Matching Variants"),
//                 fieldname: "selected_items",
//                 fieldtype: "MultiCheck",
//                 options: matching_items.map(item => ({
//                     label: `${item.item_code} - ${item.item_name}`,
//                     value: item.item_code
//                 }))
//             }
//         ],
//         primary_action_label: __("Add Selected Variants"),
//         primary_action(values) {
//             if (!values.selected_items || values.selected_items.length === 0) {
//                 frappe.msgprint(__("Please select at least one variant."));
//                 return;
//             }

//             console.log("✅ Adding selected variants to Sales Order:", values.selected_items);

//             let existing_items = frm.doc.items.map(i => i.item_code);
//             values.selected_items.forEach(item_code => {
//                 if (!existing_items.includes(item_code)) {
//                     let child = frm.add_child("items");
//                     child.item_code = item_code;
//                 }
//             });

//             frm.refresh_field("items");
//             dialog.hide();
//         }
//     });

//     dialog.show();
// }



// frappe.ui.form.on("Sales Order", {
//     refresh: function (frm) {
//         console.log("✅ Client script loaded successfully!");

//         if (frm.fields_dict.custom_add_items_from_item_template) {
//             frm.fields_dict.custom_add_items_from_item_template.$wrapper.on('click', function () {
//                 console.log("🛠 Custom Button Clicked! Running `show_item_selection_dialog` function...");
//                 show_item_selection_dialog(frm);
//             });
//         }
//     }
// });

// // Function to display the Item Template selection dialog
// function show_item_selection_dialog(frm) {
//     let d = new frappe.ui.Dialog({
//         title: __("Select Item Template"),
//         fields: [
//             {
//                 label: __("Item Template"),
//                 fieldname: "item_code",
//                 fieldtype: "Link",
//                 options: "Item",
//                 reqd: 1,
//                 get_query: function () {
//                     return {
//                         filters: {
//                             "has_variants": 1
//                         }
//                     };
//                 }
//             }
//         ],
//         primary_action_label: __("Find Variants"),
//         primary_action(values) {
//             if (!values.item_code) {
//                 frappe.msgprint(__("Please select an item template."));
//                 return;
//             }

//             console.log("🔍 Fetching attributes for item template:", values.item_code);

//             frappe.call({
//                 method: "mohan_impex.item_attr.get_item_template_attributes",
//                 args: { item_code: values.item_code },
//                 callback: function (r) {
//                     if (r.message && Object.keys(r.message).length > 0) {
//                         d.hide();
//                         console.log("✅ Attributes retrieved:", r.message);
//                         show_attribute_selection_dialog(frm, values.item_code, r.message[values.item_code]);
//                     } else {
//                         frappe.msgprint(__("No attributes found for this item template."));
//                     }
//                 }
//             });
//         }
//     });

//     d.show();
// }

// // Function to display the attribute selection dialog
// function show_attribute_selection_dialog(frm, item_code, attributes) {
//     function slugify(text) {
//         return text.toLowerCase().replace(/\s+/g, "_").replace(/[^a-z0-9_]/g, "");
//     }

//     let fields = [
//         {
//             label: __("Selected Item Template"),
//             fieldname: "selected_item_display",
//             fieldtype: "HTML",
//             options: `<div style="font-weight: bold; padding: 8px; background-color: #f5f5f5; border: 1px solid #ddd;">📌 Selected: ${item_code}</div>`,
//         },
//         {
//             label: __("Matching Variants"),
//             fieldname: "matching_variants_display",
//             fieldtype: "HTML",
//             options: `<div id="matching-variants" style="padding: 8px; background-color: #fff; border: 1px solid #ddd;">🔍 Select attributes to see matching variants...</div>`,
//         }
//     ];

//     Object.keys(attributes).forEach(attr => {
//         fields.push({
//             label: attr,
//             fieldname: slugify(attr),
//             fieldtype: "MultiCheck",
//             options: attributes[attr].map(val => ({
//                 label: val,
//                 value: val
//             }))
//         });
//     });

//     let selectedItems = [];

//     let d = new frappe.ui.Dialog({
//         title: __("Select Attributes to Match"),
//         fields: fields,
//         primary_action_label: __("Add Selected Variants"),
//         primary_action() {
//             if (selectedItems.length === 0) {
//                 frappe.msgprint(__("Please select at least one variant."));
//                 return;
//             }

//             console.log("✅ Adding selected variants to Sales Order:", selectedItems);

//             selectedItems.forEach(item_code => {
//                 let child = frm.add_child("items");
//                 child.item_code = item_code;
//             });

//             frm.refresh_field("items");
//             d.hide();
//         }
//     });

//     d.$wrapper.on("change", "input[type=checkbox]", function () {
//         let values = d.get_values();
//         console.log("🎯 Attributes Changed:", values);
//         update_matching_items(frm, item_code, values, d, selectedItems);
//     });

//     d.show();
// }

// // Function to update matching items and track selected variants
// function update_matching_items(frm, selected_item, selected_attributes, dialog, selectedItems) {
//     console.log("🔎 Updating Matching Items for:", selected_item, "with attributes:", selected_attributes);

//     frappe.call({
//         method: "mohan_impex.item_attr.get_matching_items",
//         args: {
//             selected_item: selected_item,
//             selected_attributes: JSON.stringify(selected_attributes)
//         },
//         callback: function (r) {
//             let container = document.getElementById("matching-variants");
//             if (!container) return;

//             if (r.message && r.message.length > 0) {
//                 console.log("✅ Matching variants found:", r.message);
//                 let htmlContent = `
//                     <button id="select-all-variants" style="margin-bottom: 5px; padding: 5px; background-color: #007bff; color: #fff; border: none; cursor: pointer;">✔ Select All</button>
//                     <ul style="padding: 0; list-style: none;">`;

//                 r.message.forEach(item => {
//                     htmlContent += `<li style="padding: 5px 0; border-bottom: 1px solid #ddd;">
//                         <input type="checkbox" name="selected_variants" value="${item.item_code}"> 
//                         ${item.item_code}
//                     </li>`;
//                 });

//                 htmlContent += `</ul>`;
//                 container.innerHTML = htmlContent;

//                 let checkboxes = container.querySelectorAll("input[name='selected_variants']");
//                 let selectAllButton = document.getElementById("select-all-variants");

//                 // Handle "Select All" functionality
//                 selectAllButton.addEventListener("click", function () {
//                     let allChecked = Array.from(checkboxes).every(cb => cb.checked);
//                     checkboxes.forEach(cb => cb.checked = !allChecked);
//                     updateSelectedItems(checkboxes, selectedItems);
//                 });

//                 // Handle individual checkbox changes
//                 checkboxes.forEach(checkbox => {
//                     checkbox.addEventListener("change", function () {
//                         updateSelectedItems(checkboxes, selectedItems);
//                     });
//                 });

//             } else {
//                 container.innerHTML = `<div style="padding: 8px; background-color: #f5f5f5; border: 1px solid #ddd;">❌ No matching variants found.</div>`;
//             }
//         }
//     });
// }

// // Function to update selected items dynamically **without resetting the array**
// function updateSelectedItems(checkboxes, selectedItems) {
//     let newSelectedItems = new Set(selectedItems); // Preserve previous selections

//     checkboxes.forEach(cb => {
//         if (cb.checked) {
//             newSelectedItems.add(cb.value);
//         } else {
//             newSelectedItems.delete(cb.value);
//         }
//     });

//     // Convert back to array and update selected items
//     selectedItems.length = 0;  // Clear array but keep reference
//     selectedItems.push(...newSelectedItems);

//     console.log("✅ Updated selected items:", selectedItems);
// }


frappe.ui.form.on("Sales Order", {
    refresh: function (frm) {
        console.log("✅ Client script loaded successfully!");

        if (frm.fields_dict.custom_add_items_from_item_template) {
            frm.fields_dict.custom_add_items_from_item_template.$wrapper.on('click', function () {
                console.log("🛠 Custom Button Clicked! Running `show_item_selection_dialog` function...");
                show_combined_dialog(frm);
            });
        }
    }
});

// Function to display the combined dialog with Item Template, Attributes, and Matching Variants
function show_combined_dialog(frm) {
    let selectedItems = [];
    let attributes = {};
    let matchingVariants = [];
    
    let d = new frappe.ui.Dialog({
        title: __("Select Items"),
        size: "extra-large",
        fields: [
            // Section 1: Item Template Selection
            {
                label: __("Item Template"),
                fieldname: "item_code",
                fieldtype: "Link",
                options: "Item",
                reqd: 1,
                get_query: function () {
                    return { filters: { "has_variants": 1 } };
                }
            },
            {
                fieldtype: "Section Break",
                label: "Select Attributes",
                fieldname: "attribute_section"
            },
            {
                fieldname: "attribute_container",
                fieldtype: "HTML",
                options: `<div id='attribute-fields'></div>`
            },
            {
                fieldtype: "Section Break",
                label: "Matching Variants",
                fieldname: "matching_section"
            },
            {
                fieldname: "matching_variants_display",
                fieldtype: "HTML",
                options: `<div id='matching-variants'></div>`
            }
        ],
        primary_action_label: __("Add Selected Variants"),
        primary_action() {
            let selectedCheckboxes = d.$wrapper.find("input[name='selected_variants']:checked");
            selectedItems = Array.from(selectedCheckboxes).map(cb => cb.value);
            
            if (selectedItems.length === 0) {
                frappe.msgprint(__("Please select at least one variant."));
                return;
            }
            
            console.log("✅ Adding selected variants to Sales Order:", selectedItems);
            selectedItems.forEach(item_code => {
                let child = frm.add_child("items");
                child.item_code = item_code;
            });
            frm.refresh_field("items");
            d.hide();
        }
    });

    // Fetch attributes when item is selected
    d.fields_dict.item_code.df.onchange = function () {
        let item_code = d.get_value("item_code");
        if (!item_code) return;

        console.log("🔍 Fetching attributes for item template:", item_code);

        frappe.call({
            method: "mohan_impex.item_attr.get_item_template_attributes",
            args: { item_code: item_code },
            callback: function (r) {
                if (r.message && Object.keys(r.message).length > 0) {
                    attributes = r.message[item_code];
                    render_attribute_fields(d, attributes);
                } else {
                    frappe.msgprint(__("No attributes found for this item template."));
                }
            }
        });
    };

    d.show();
}

// Function to dynamically render attributes
function render_attribute_fields(dialog, attributes) {
    let container = dialog.fields_dict.attribute_container.$wrapper;
    container.html("");
    let fields = "";

    Object.keys(attributes).forEach(attr => {
        fields += `<div style='padding: 8px 0; font-weight: bold;'>${attr}</div>`;
        attributes[attr].forEach(val => {
            let fieldname = `attr_${attr.replace(/\s+/g, '_').toLowerCase()}`;
            fields += `<label><input type='checkbox' name='${fieldname}' value='${val}'> ${val}</label><br>`;
        });
    });
    container.html(fields);

    // Update matching items dynamically
    container.find("input[type=checkbox]").on("change", function () {
        let selectedAttributes = {};
        container.find("input[type=checkbox]:checked").each(function () {
            let key = this.name.replace("attr_", "");
            if (!selectedAttributes[key]) selectedAttributes[key] = [];
            selectedAttributes[key].push(this.value);
        });
        update_matching_items(dialog, selectedAttributes);
    });
}

// Function to update matching items dynamically
function update_matching_items(dialog, selectedAttributes) {
    let item_code = dialog.get_value("item_code");
    console.log("🔎 Updating Matching Items for:", item_code, "with attributes:", selectedAttributes);

    frappe.call({
        method: "mohan_impex.item_attr.get_matching_items",
        args: {
            selected_item: item_code,
            selected_attributes: JSON.stringify(selectedAttributes)
        },
        callback: function (r) {
            let container = document.getElementById("matching-variants");
            if (!container) {
                console.error("❌ Error: `#matching-variants` container not found.");
                return;
            }

            if (r.message && r.message.length > 0) {
                console.log("✅ Matching variants found:", r.message);
                
                let htmlContent = `<ul style='padding: 0; list-style: none; max-height: 200px; overflow-y: auto;'>`;
                r.message.forEach(item => {
                    htmlContent += `<li style='padding: 5px 0;'>
                        <input type='checkbox' name='selected_variants' value='${item.item_code}'> 
                        ${item.item_code}
                    </li>`;
                });
                htmlContent += `</ul>`;
                container.innerHTML = htmlContent;
            } else {
                container.innerHTML = `<div style='padding: 8px; background-color: #f5f5f5; border: 1px solid #ddd;'>❌ No matching variants found.</div>`;
            }
        }
    });
}
