import frappe
@frappe.whitelist()
def update_variant_brands(item_template, brands):
    import json
    # convert stringified list (if needed) to Python list
    if isinstance(brands, str):
        brands = json.loads(brands)

    variants = frappe.get_all("Item", filters={"variant_of": item_template}, pluck="name")

    for variant in variants:
        doc = frappe.get_doc("Item", variant)
        doc.set("custom_select_brand", [])  # Clear existing
        for row in brands:
            doc.append("custom_select_brand", {
                "brand_item": row.get("brand_item")
            })
        doc.save()

    return True


