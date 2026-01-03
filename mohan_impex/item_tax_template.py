import frappe

@frappe.whitelist()
def get_tax_template_by_item(item_code):
    if not item_code:
        return None

    if not frappe.db.exists("Item", item_code):
        return None

    # Item -> Item Tax child table
    item_tax_template = frappe.db.get_value(
        "Item Tax",
        {"parent": item_code, "parenttype": "Item", "parentfield": "taxes"},
        "item_tax_template",
    )
    return item_tax_template


def set_item_tax_templates(doc):
    # adjust child table fieldname if different
    for row in (doc.items or []):
        if row.item_code and not row.item_tax_template:
            row.item_tax_template = get_tax_template_by_item(row.item_code)


def validate(doc, method=None):
    set_item_tax_templates(doc)
