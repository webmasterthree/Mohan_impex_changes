import frappe
from frappe.utils import flt
@frappe.whitelist()
def create_secondary_stock_entry():
    try:
        # 1. Create Secondary Stock Entry
        se_doc = frappe.get_doc({
            "doctype": "Secondary Stock Entry",
            "item_code": frappe.form_dict.get("item_code"),
            "stock_uom": frappe.form_dict.get("stock_uom"),
            "actual_qty": frappe.form_dict.get("actual_qty"),
            "warehouse": frappe.form_dict.get("warehouse"),
            "customer": frappe.form_dict.get("customer"),
        }).insert()

        # 2. Auto-create matching Secondary Stock Bin
        bin_doc = frappe.get_doc({
            "doctype": "Secondary Stock Bin",
            "item_code": se_doc.item_code,
            "stock_uom": se_doc.stock_uom,
            "actual_qty": se_doc.actual_qty,
            "warehouse": se_doc.warehouse,
            "customer": se_doc.customer,
        }).insert()

        # Response (optional)
        frappe.local.response["status"] = True
        frappe.local.response["message"] = "Secondary Stock Entry & Bin records created"
        frappe.local.response["data"] = [{
            "secondary_stock_entry": se_doc.name,
            "secondary_stock_bin": bin_doc.name,
        }]

    except Exception as err:
        get_exception(err)



def on_submit(doc, method):
    for row in doc.items:

        # Find Secondary Stock Bin (match item_code + stock_uom + customer ONLY)
        bin_name = frappe.db.get_value(
            "Secondary Stock Bin",
            {
                "item_code": row.item_code,
                "stock_uom": row.uom,
                "customer": doc.customer
            },
            "name"
        )

        if not bin_name:
            frappe.throw(
                f"No Stock found for Item {row.item_code}, "
                f"UOM {row.uom}, Customer {doc.customer}"
            )

        bin_doc = frappe.get_doc("Secondary Stock Bin", bin_name)

        current_qty = flt(bin_doc.actual_qty)
        qty_to_deduct = flt(row.qty)

        # Optional: Stock validation
        if current_qty < qty_to_deduct:
            frappe.throw(
                f"Not enough stock for Item {row.item_code}. "
                f"Available: {current_qty}, Required: {qty_to_deduct}"
            )

        # Deduct stock
        bin_doc.actual_qty = current_qty - qty_to_deduct
        bin_doc.save()
