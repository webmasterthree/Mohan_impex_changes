import frappe

@frappe.whitelist()
def exim_data(delivery_note: str):

	if not delivery_note:
		frappe.throw("delivery_note is required")

	dn = frappe.get_doc("Delivery Note", delivery_note)

	sales_order = ""
	for row in (dn.items or []):
		if row.against_sales_order:
			sales_order = row.against_sales_order
			break

	fields_to_fetch = [
		"shipping_terms",
		"port_of_loading",
		"port_of_discharge",
		"country_of_origin",
		"country_of_destination",
		"shipping_instructions",
		"pre_carriage_by",
		"place_of_precarrier",
		"marks_and_no",
	]

	out = {
		"delivery_note": dn.name or "",
		"sales_order": sales_order,
	}

	for f in fields_to_fetch:
		out[f] = ""

	if not sales_order:
		return out

	so = frappe.db.get_value("Sales Order", sales_order, fields_to_fetch, as_dict=True) or {}

	for f in fields_to_fetch:
		out[f] = "" if so.get(f) is None else so.get(f)

	return out