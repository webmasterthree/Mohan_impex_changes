# import frappe
# from frappe import _

# @frappe.whitelist()
# def get_item_attributes(item_code):
#     """
#     Fetch attributes for the selected item.
#     """
#     try:
#         attributes = frappe.db.get_all(
#             "Item Variant Attribute",
#             filters={"parent": item_code},
#             fields=["attribute"]
#         )

#         for attr in attributes:
#             attribute_data = frappe.get_doc("Item Attribute", attr["attribute"])
#             attr["values"] = [{"attribute_value": val.attribute_value, "abbr": val.abbr}
#                               for val in attribute_data.item_attribute_values]

#         return {"attributes": attributes}

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error fetching item attributes"))
#         return {"status": "error", "message": str(e)}

# @frappe.whitelist()
# def get_matching_items(selected_item, selected_attributes):
#     """
#     Fetch items that have matching attributes similar to the selected item.
#     """
#     try:
#         attributes = frappe.parse_json(selected_attributes)
#         if not attributes:
#             return []

#         # Get all items except the selected item
#         items = frappe.db.get_all(
#             "Item",
#             filters={"variant_of": selected_item},
#             fields=["item_code", "item_name"]
#         )

#         matching_items = []

#         selected_attr_values = {attr.lower(): [val.lower() for val in attributes[attr]] for attr in attributes}

#         for item in items:
#             # Fetch attributes for this item
#             item_attributes = frappe.db.get_all(
#                 "Item Variant Attribute",
#                 filters={"parent": item["item_code"]},
#                 fields=["attribute", "attribute_value"]
#             )

#             item_attr_dict = {attr["attribute"].lower(): attr["attribute_value"].lower() for attr in item_attributes}

#             # Check if all selected attributes match (handling lists & case sensitivity)
#             is_match = all(
#                 item_attr_dict.get(attr, "") in selected_attr_values[attr]
#                 for attr in selected_attr_values
#             )

#             if is_match:
#                 matching_items.append(item)

#         return matching_items

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error fetching matching items"))
#         return []


# import frappe
# from frappe import _

# @frappe.whitelist()
# def get_item_attributes(item_code):
#     """
#     Fetch attributes for the selected item, but only return the values assigned to this specific item.
#     """
#     try:
#         attributes = frappe.db.get_all(
#             "Item Variant Attribute",
#             filters={"parent": item_code},
#             fields=["attribute", "attribute_value"]
#         )

#         result = []
#         for attr in attributes:
#             attribute_data = frappe.get_doc("Item Attribute", attr["attribute"])
            
#             # Find only the values assigned to this item
#             assigned_values = [
#                 {"attribute_value": val.attribute_value, "abbr": val.abbr}
#                 for val in attribute_data.item_attribute_values
#                 if val.attribute_value == attr["attribute_value"]  # Ensure only assigned values are included
#             ]

#             # Append only if there are values assigned
#             if assigned_values:
#                 result.append({
#                     "attribute": attr["attribute"],
#                     "values": assigned_values
#                 })

#         return {"attributes": result}

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error fetching item attributes"))
#         return {"status": "error", "message": str(e)}

# @frappe.whitelist()
# def get_matching_items(selected_item, selected_attributes):
#     """
#     Fetch items that have matching attributes similar to the selected item.
#     """
#     try:
#         attributes = frappe.parse_json(selected_attributes)
#         if not attributes:
#             return []

#         # Get all variants of the selected item
#         items = frappe.db.get_all(
#             "Item",
#             filters={"variant_of": selected_item},
#             fields=["item_code", "item_name"]
#         )

#         matching_items = []
#         selected_attr_values = {attr.lower(): [val.lower() for val in attributes[attr]] for attr in attributes}

#         for item in items:
#             # Fetch attributes for this item
#             item_attributes = frappe.db.get_all(
#                 "Item Variant Attribute",
#                 filters={"parent": item["item_code"]},
#                 fields=["attribute", "attribute_value"]
#             )

#             item_attr_dict = {attr["attribute"].lower(): attr["attribute_value"].lower() for attr in item_attributes}

#             # Check if all selected attributes match
#             is_match = all(
#                 item_attr_dict.get(attr, "") in selected_attr_values[attr]
#                 for attr in selected_attr_values
#             )

#             if is_match:
#                 matching_items.append(item)

#         return matching_items

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error fetching matching items"))
#         return []





# import frappe
# from frappe import _

# @frappe.whitelist()
# def get_item_attributes(item_code):
#     """
#     Fetch attributes for the selected item.
#     """
#     try:
#         attributes = frappe.db.get_all(
#             "Item Variant Attribute",
#             filters={"parent": item_code},
#             fields=["attribute"]
#         )

#         for attr in attributes:
#             attribute_data = frappe.get_doc("Item Attribute", attr["attribute"])
#             attr["values"] = [{"attribute_value": val.attribute_value, "abbr": val.abbr}
#                               for val in attribute_data.item_attribute_values]

#         return {"attributes": attributes}

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error fetching item attributes"))
#         return {"status": "error", "message": str(e)}

# @frappe.whitelist()
# def get_matching_items(selected_item, selected_attributes):
#     """
#     Fetch items that have matching attributes similar to the selected item.
#     """
#     try:
#         attributes = frappe.parse_json(selected_attributes)
#         if not attributes:
#             return []

#         # Get all items except the selected item
#         items = frappe.db.get_all(
#             "Item",
#             filters={"variant_of": selected_item},
#             fields=["item_code", "item_name"]
#         )

#         matching_items = []

#         selected_attr_values = {attr.lower(): [val.lower() for val in attributes[attr]] for attr in attributes}

#         for item in items:
#             # Fetch attributes for this item
#             item_attributes = frappe.db.get_all(
#                 "Item Variant Attribute",
#                 filters={"parent": item["item_code"]},
#                 fields=["attribute", "attribute_value"]
#             )

#             item_attr_dict = {attr["attribute"].lower(): attr["attribute_value"].lower() for attr in item_attributes}

#             # Check if all selected attributes match (handling lists & case sensitivity)
#             is_match = all(
#                 item_attr_dict.get(attr, "") in selected_attr_values[attr]
#                 for attr in selected_attr_values
#             )

#             if is_match:
#                 matching_items.append(item)

#         return matching_items

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), _("Error fetching matching items"))
#         return []

import frappe
from frappe import _

@frappe.whitelist()
def get_matching_items(selected_item, selected_attributes="{}"):
    """
    Fetch items that are variants of the selected item template.
    """
    try:
        # Get all item variants of the selected template
        items = frappe.db.get_all(
            "Item",
            filters={"variant_of": selected_item},
            fields=["item_code", "item_name"]
        )

        return items if items else []

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error fetching matching items"))
        return []
