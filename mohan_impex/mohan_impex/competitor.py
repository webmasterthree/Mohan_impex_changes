import frappe


def add_others_in_competitor_item(doc, method):
    if not any(d.item_name == "Others" for d in doc.competitor_item):
        doc.append("competitor_item", {"item_name": "Others"})