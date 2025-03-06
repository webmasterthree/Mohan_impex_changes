// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

// frappe.query_reports["Leave Status Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Leave Status Report"] = {
    "filters": [
        {
            "fieldname": "start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "default":frappe.datetime.get_today(),
            "reqd": 0  // Required field
        },
        {
            "fieldname": "end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "default":frappe.datetime.get_today(),
            "reqd": 0  // Required field
        }
    ]
};
