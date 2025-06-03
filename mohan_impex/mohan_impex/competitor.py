import frappe


def add_others_in_competitor_item(doc, method):
    if not any(d.item_name == "Other" for d in doc.competitor_item):
        doc.append("competitor_item", {"item_name": "Other"})