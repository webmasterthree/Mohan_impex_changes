
# @frappe.whitelist()
# def get_delivery_note_from_sales_invoice(name):
#     if not name:
#         return None

#     row = frappe.get_all(
#         "Sales Invoice Item",
#         filters={"parent": name},
#         fields=["delivery_note"],
#         order_by="idx asc",
#         limit=1
#     )

#     return row[0].delivery_note if row else None
import frappe

@frappe.whitelist()
def get_delivery_note_from_sales_invoice(name):
    """Return Delivery Note and related Purchase Invoices (transporter / misc / labour).

    Output example:
    {
        "delivery_note": "DN-25-00110",
        "transporter": {
            "name": "PUR-TRN-0001-25-26",
            "rounded_total": 1234.0
        },
        "misc_expense": {
            "name": "PUR-MISC-0002-25-26",
            "rounded_total": 500.0
        },
        "labour_payment": {
            "name": "PUR-LBR-0003-25-26",
            "rounded_total": 800.0
        }
    }
    """
    if not name:
        return {}

    # Get first Sales Invoice Item to read its Delivery Note
    si_item = frappe.get_all(
        "Sales Invoice Item",
        filters={"parent": name},
        fields=["delivery_note"],
        order_by="idx asc",
        limit=1,
    )

    if not si_item or not si_item[0].delivery_note:
        return {}

    delivery_note = si_item[0].delivery_note

    def get_pi_for_field(fieldname):
        """Fetch first Purchase Invoice where <fieldname> = delivery_note."""
        pi = frappe.get_all(
            "Purchase Invoice",
            filters={fieldname: delivery_note},
            fields=["name", "rounded_total"],
            limit=1,
        )
        return pi[0] if pi else None

    transporter_pi = get_pi_for_field("dn_transporter_payment")
    misc_pi = get_pi_for_field("dn_misc_expense")
    labour_pi = get_pi_for_field("dn_labour_payment")

    return {
        "delivery_note": delivery_note,
        "transporter": transporter_pi,
        "misc_expense": misc_pi,
        "labour_payment": labour_pi,
    }
