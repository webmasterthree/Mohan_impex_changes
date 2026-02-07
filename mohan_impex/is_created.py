import frappe

@frappe.whitelist()
def is_link_name_exists(link_name: str, service_payment_type: str) -> bool:
    link_name = (link_name or "").strip()
    service_payment_type = (service_payment_type or "").strip()

    # Mandatory checks
    if not link_name or not service_payment_type:
        return False

    exists = frappe.db.sql(
        """
        SELECT 1
        FROM `tabPayment Doc Type` lnk
        INNER JOIN `tabPurchase Invoice` pi
            ON pi.name = lnk.parent
        WHERE lnk.link_name = %(link_name)s
          AND pi.service_payment_type = %(service_payment_type)s
          AND pi.docstatus != 2
        LIMIT 1
        """,
        {
            "link_name": link_name,
            "service_payment_type": service_payment_type
        }
    )

    return bool(exists)
