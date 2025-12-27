import frappe

@frappe.whitelist()
def misc_payment_entry(purchase_receipt):
    if not purchase_receipt:
        frappe.throw("Purchase Receipt is required")

    # Get full document including child table
    pr = frappe.get_doc("Purchase Receipt", purchase_receipt)

    # Build a clean response
    data = {
        "name": pr.name,
        "misc_supplier": pr.get("misc_supplier"),
        "total_misc_amount": pr.get("total_misc_amount") or 0,
        "miscellaneous_expenses": []
    }

    # Loop through child table: miscellaneous_expenses
    for row in pr.get("miscellaneous_expenses") or []:
        data["miscellaneous_expenses"].append({
            "item_name": row.item_name,
            "item_details": row.item_details,
            "misc_item_template": row.misc_item_template,
            "qty": row.qty,
            "rate": row.rate,
            "amount": row.amount,
            "uom": row.uom,
        })

    return data




@frappe.whitelist()
def has_transporter_payment(transporter_payment):
    if not transporter_payment:
        return False

    exists = frappe.db.exists(
        "Purchase Invoice",
        {
            "transporter_payment": transporter_payment,
            "docstatus": ["!=", 2]
        }
    )

    return True if exists else False

@frappe.whitelist()
def has_labour_payment(grn):
    if not grn:
        return False

    exists = frappe.db.exists(
        "Purchase Invoice",
        {
            "grn": grn,
            "docstatus": ["!=", 2]
        }
    )

    return True if exists else False


@frappe.whitelist()
def has_misc_payment(misc_expense):
    if not misc_expense:
        return False

    exists = frappe.db.exists(
        "Purchase Invoice",
        {
            "misc_expense": misc_expense,
            "docstatus": ["!=", 2]
        }
    )

    return True if exists else False





# Selling Payment

@frappe.whitelist()
def misc_dn_payment_entry(name):
    if not name:
        frappe.throw("Delivery Note id is required")

    # Get full document including child table
    pr = frappe.get_doc("Delivery Note", name)

    # Build a clean response
    data = {
        "name": pr.name,
        "misc_supplier": pr.get("misc_supplier"),
        "total_misc_amount": pr.get("total_misc_amount") or 0,
        "miscellaneous_expenses": []
    }

    # Loop through child table: miscellaneous_expenses
    for row in pr.get("miscellaneous_expenses") or []:
        data["miscellaneous_expenses"].append({
            "item_name": row.item_name,
            "item_details": row.item_details,
            "misc_item_template": row.misc_item_template,
            "qty": row.qty,
            "rate": row.rate,
            "amount": row.amount,
            "uom": row.uom,
        })

    return data




@frappe.whitelist()
def has_dn_transporter_payment(dn_transporter_payment):
    if not dn_transporter_payment:
        return False

    exists = frappe.db.exists(
        "Purchase Invoice",
        {
            "dn_transporter_payment": dn_transporter_payment,
            "docstatus": ["!=", 2]
        }
    )

    return True if exists else False

@frappe.whitelist()
def has_dn_labour_payment(dn_labour_payment):
    if not dn_labour_payment:
        return False

    exists = frappe.db.exists(
        "Purchase Invoice",
        {
            "dn_labour_payment": dn_labour_payment,
            "docstatus": ["!=", 2]
        }
    )

    return True if exists else False


@frappe.whitelist()
def has_dn_misc_payment(dn_misc_expense):
    if not dn_misc_expense:
        return False

    exists = frappe.db.exists(
        "Purchase Invoice",
        {
            "dn_misc_expense": dn_misc_expense,
            "docstatus": ["!=", 2]
        }
    )

    return True if exists else False
