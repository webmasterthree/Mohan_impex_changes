import frappe
from frappe import _

from erpnext.accounts.utils import get_item_tax_template

@frappe.whitelist()
def get_tax_template_by_item(item_code):
    if not item_code:
        frappe.throw(_("Item Code is required"))

    # Get default company
    company = frappe.defaults.get_user_default("company") or \
              frappe.db.get_single_value("Global Defaults", "default_company")

    if not company:
        frappe.throw(_("Default Company is not set"))

    # Call ERPNext function
    res = get_item_tax_template({
        "item_code": item_code,
        "company": company
    })

    return res
