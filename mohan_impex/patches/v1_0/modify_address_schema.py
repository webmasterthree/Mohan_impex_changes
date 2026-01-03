import frappe

def execute():
    """
    Patch to update 'Address' DocType:
    - Convert 'city' field from Data → Link (City)
    - Convert 'state' field from Data → Link (State)
      only if 'India Compliance' app is NOT installed
    """

    doctype = "Address"

    # Always update 'city'
    _create_or_update_property_setter(doctype, "city", "fieldtype", "Link", "Data")
    _create_or_update_property_setter(doctype, "city", "options", "City", "Data")
    frappe.logger().info("✅ Updated Address.city → Link(City)")

    # Update 'state' only if India Compliance app not installed
    if not _is_india_compliance_installed():
        _create_or_update_property_setter(doctype, "state", "fieldtype", "Link", "Data")
        _create_or_update_property_setter(doctype, "state", "options", "State", "Data")
        frappe.logger().info("✅ Updated Address.state → Link(State)")
    else:
        frappe.logger().info("⚠️ Skipped Address.state update (India Compliance app found)")

    frappe.clear_cache(doctype=doctype)
    frappe.reload_doc("contacts", "doctype", "address")

    frappe.logger().info("✅ Address.city/state link update completed successfully.")


def _is_india_compliance_installed():
    """Return True if 'India Compliance' app is installed."""
    installed_apps = frappe.get_installed_apps()
    return any("india_compliance" in app.lower() for app in installed_apps)


def _create_or_update_property_setter(doctype, fieldname, property_name, value, property_type):
    """Create or update a Property Setter cleanly and safely."""
    existing = frappe.db.exists(
        "Property Setter",
        {"doc_type": doctype, "field_name": fieldname, "property": property_name},
    )

    if existing:
        existing_doc = frappe.get_doc("Property Setter", existing)
        if str(existing_doc.value) != str(value):
            existing_doc.value = value
            existing_doc.save(ignore_permissions=True)
            frappe.logger().info(
                f"🔄 Updated Property Setter: {doctype}.{fieldname}.{property_name} → {value}"
            )
    else:
        frappe.make_property_setter({
            "doctype": doctype,
            "fieldname": fieldname,
            "property": property_name,
            "value": value,
            "property_type": property_type,
        })
        frappe.logger().info(
            f"🆕 Created Property Setter: {doctype}.{fieldname}.{property_name} → {value}"
        )
