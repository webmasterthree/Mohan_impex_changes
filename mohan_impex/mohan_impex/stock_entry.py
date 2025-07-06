import frappe
from frappe.utils import flt
import json

def inspection_validation(self, method):
    if self.product_inspection_required:
        for idx, item in enumerate(self.items, 1):
            if not item.product_inspection and self.product_inspection_required:
                frappe.throw(
                    title="Product Testing Inspection Required",
                    msg=f"Row #{idx}: Product Testing Inspection required for <strong>{item.item_name}</strong>"
                )
    if self.application_inspection_required:
        for idx, item in enumerate(self.items, 1):
            if not item.application_inspection and self.application_inspection_required:
                frappe.throw(
                    title="Application Testing Inspection Required",
                    msg=f"Row #{idx}: Application Testing Inspection required for <strong>{item.item_name}</strong>"
                )

@frappe.whitelist()
def check_item_quality_inspection(doctype, items, inspection_scope):
	if isinstance(items, str):
		items = json.loads(items)

	inspection_fieldname_map = {
		"Purchase Receipt": "inspection_required_before_purchase",
		"Purchase Invoice": "inspection_required_before_purchase",
		"Subcontracting Receipt": "inspection_required_before_purchase",
		"Sales Invoice": "inspection_required_before_delivery",
		"Delivery Note": "inspection_required_before_delivery",
	}

	items_to_remove = []
	for item in items:
		if not frappe.db.get_value("Item", item.get("item_code"), inspection_fieldname_map.get(doctype)):
			items_to_remove.append(item)
	items = [item for item in items if item not in items_to_remove]

	return items

@frappe.whitelist()
def make_quality_inspections(doctype, docname, items, scope):
	if isinstance(items, str):
		items = json.loads(items)

	inspections = []
	for item in items:
		if flt(item.get("sample_size")) > flt(item.get("qty")):
			frappe.throw(
				_(
					"{item_name}'s Sample Size ({sample_size}) cannot be greater than the Accepted Quantity ({accepted_quantity})"
				).format(
					item_name=item.get("item_name"),
					sample_size=item.get("sample_size"),
					accepted_quantity=item.get("qty"),
				)
			)

		quality_inspection = frappe.get_doc(
			{
				"doctype": "Quality Inspection",
                "inspection_scope": scope,
				"inspection_type": "Incoming",
				"inspected_by": frappe.session.user,
				"reference_type": doctype,
				"reference_name": docname,
				"item_code": item.get("item_code"),
				"description": item.get("description"),
				"sample_size": flt(item.get("sample_size")),
				"item_serial_no": item.get("serial_no").split("\n")[0] if item.get("serial_no") else None,
				"batch_no": item.get("batch_no"),
			}
		).insert()
		quality_inspection.save()
		inspections.append(quality_inspection.name)

	return inspections
