// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.query_reports["Proof of Delivery Status"] = {
	"filters": [
		{
			"fieldname": "proof_of_delivery_status",
			"label": "Proof of Delivery Status",
			"fieldtype": "Select",
			"options": [
				"",
				"Pending",
				"Uploaded",
				"Verified",
			],
			"default": "Pending"
		}
	]
};
