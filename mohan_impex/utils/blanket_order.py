import frappe
import json
from frappe.utils import flt, today


@frappe.whitelist()
def update_items(blanket_order, items, from_date):
	items = json.loads(items)

	doc = frappe.get_doc("Blanket Order", blanket_order)
	doc.from_date = from_date

	if doc.workflow_state != "Open":
		frappe.throw("Blanket Order must be Open to update items")

	doc.flags.ignore_validate_update_after_submit = True

	existing_rows = {row.name: row for row in doc.items}

	for row in items:
		row_name = row.get("name")
		if not row_name or row_name not in existing_rows:
			continue

		doc_row = existing_rows[row_name]
		item_changed = row.get("item_code") != doc_row.item_code

		if item_changed:
			doc.append("custom_blanket_order_item_history", {
				"item_code": doc_row.item_code,
				"item_name": doc_row.item_name,
				"qty": doc_row.qty,
				"rate": doc_row.rate,
				"ordered_qty": doc_row.ordered_qty,
				"replaced_on": today(),
				"replaced_by": row.get("item_code")
			})

			doc_row.item_code = row.get("item_code")
			doc_row.item_name = frappe.get_value(
				"Item", row.get("item_code"), "item_name"
			)
			doc_row.ordered_qty = 0

		if not item_changed:
			if flt(row.get("qty")) < flt(doc_row.ordered_qty):
				frappe.throw(
					f"Quantity cannot be less than ordered quantity "
					f"for item {doc_row.item_code}"
				)

		doc_row.qty = flt(row.get("qty"))
		doc_row.rate = flt(row.get("rate"))

	doc.save(ignore_permissions=True)
