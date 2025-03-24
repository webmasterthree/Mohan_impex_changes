import frappe
from frappe import _

@frappe.whitelist()
def get_purchase_order_items(purchase_order=None):
    """Fetch item details including shelf life from a specific Purchase Order"""

    try:
        if not purchase_order:
            return {"status": "error", "message": _("Purchase Order is required.")}

        # Fetch item details from the Purchase Order Item table
        items = frappe.db.get_all(
            "Purchase Order Item",
            filters={"parent": purchase_order},
            fields=["item_code", "qty", "uom", "rate"]
        )

        if not items:
            return {"status": "error", "message": _("No items found for this Purchase Order.")}

        # Get item codes as a list
        item_codes = [item["item_code"] for item in items]

        # Fetch shelf life from Item master
        item_details = frappe.db.get_all(
            "Item",
            filters={"item_code": ["in", item_codes]},
            fields=["item_code", "shelf_life_in_days"]
        )

        # Create a mapping of item codes to shelf life
        item_shelf_life_map = {
            item["item_code"]: item.get("shelf_life_in_days")
            for item in item_details
        }

        # Merge shelf life details into the response
        for item in items:
            item["shelf_life_in_days"] = item_shelf_life_map.get(item["item_code"])

        return {"status": "success", "data": items}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# import frappe
# from frappe import _

# @frappe.whitelist()
# def get_purchase_order_items(purchase_order=None):
#     """Fetch item codes and their shelf life from a specific Purchase Order"""

#     try:
#         if not purchase_order:
#             return {"status": "error", "message": _("Purchase Order is required.")}

#         # Fetch item codes from the Purchase Order
#         items = frappe.db.get_all(
#             "Purchase Order Item",
#             filters={"parent": purchase_order},
#             fields=["item_code"]
#         )

#         if not items:
#             return {"status": "error", "message": _("No items found for this Purchase Order.")}

#         # Get item codes as a list
#         item_codes = [item["item_code"] for item in items]

#         # Fetch shelf life for the items
#         item_details = frappe.db.get_all(
#             "Item",
#             filters={"item_code": ["in", item_codes]},
#             fields=["item_code", "shelf_life_in_days","stock_uom"]
#         )

#         # Create a mapping of item codes to shelf life
#         item_shelf_life_map = {item["item_code"]: item["shelf_life_in_days"] for item in item_details}

#         # Merge shelf life details into the response
#         for item in items:
#             item["shelf_life_in_days"] = item_shelf_life_map.get(item["item_code"], None)

#         return {"status": "success", "data": items}

#     except Exception as e:
#         return {"status": "error", "message": str(e)}



