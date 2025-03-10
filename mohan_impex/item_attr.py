import frappe
from frappe import _

@frappe.whitelist()
def get_item_template_attributes():
    """
    API to fetch all unique attributes and values grouped by Item Templates.
    Accessible via /api/method/mohan_impex.item_attr.get_item_template_attributes
    """

    # Step 1: Fetch Item Templates (has_variants=1)
    item_templates = frappe.db.get_all("Item", 
                                       filters={"has_variants": 1}, 
                                       fields=["name"])

    template_names = [t["name"] for t in item_templates]

    # Step 2: Fetch Attributes for Variants of Each Template
    item_attributes = frappe.db.get_all("Item Variant Attribute", 
                                        filters={"variant_of": ["in", template_names]}, 
                                        fields=["variant_of", "attribute", "attribute_value"])

    # Step 3: Structure Data
    template_attributes = {}

    for attribute in item_attributes:
        template_name = attribute["variant_of"]
        attr_name = attribute["attribute"]
        attr_value = attribute["attribute_value"]

        # Initialize template if not already present
        if template_name not in template_attributes:
            template_attributes[template_name] = {}

        # Add attribute values under each template
        if attr_name not in template_attributes[template_name]:
            template_attributes[template_name][attr_name] = set()

        template_attributes[template_name][attr_name].add(attr_value)

    # Convert sets to lists for JSON compatibility
    template_attributes = {k: {attr: list(values) for attr, values in v.items()} for k, v in template_attributes.items()}

    return template_attributes


import frappe
from frappe import _

@frappe.whitelist()
def get_matching_items(selected_item=None, selected_attributes=None):
    """
    Fetch items that have matching attributes similar to the selected item.
    Accessible via /api/method/mohan_impex.item_attr.get_matching_items
    """
    try:
        if not selected_item:
            frappe.throw(_("Missing required parameter: selected_item"))

        if not selected_attributes:
            frappe.throw(_("Missing required parameter: selected_attributes"))

        attributes = frappe.parse_json(selected_attributes)  # Convert JSON string to dict

        # Fetch all item variants under the selected template
        items = frappe.db.get_all(
            "Item",
            filters={"variant_of": selected_item},
            fields=["name as item_code", "item_name"]
        )

        if not items:
            return []

        matching_items = []

        # Convert selected attribute values to lowercase for case-insensitive matching
        selected_attr_values = {attr.lower(): [val.lower() for val in values] for attr, values in attributes.items()}

        for item in items:
            # Fetch attributes for this item variant
            item_attributes = frappe.db.get_all(
                "Item Variant Attribute",
                filters={"parent": item["item_code"]},
                fields=["attribute", "attribute_value"]
            )

            # Convert item attributes to a dictionary with lowercase keys & values
            item_attr_dict = {attr["attribute"].lower(): attr["attribute_value"].lower() for attr in item_attributes}

            # Check if the item matches all selected attributes
            is_match = all(
                attr in item_attr_dict and item_attr_dict[attr] in selected_attr_values[attr]
                for attr in selected_attr_values
            )

            if is_match:
                matching_items.append(item)

        return matching_items

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching matching items"))
        return {"error": str(e)}



