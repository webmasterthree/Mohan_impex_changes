// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Attendance Report"] = {
    "filters": [
        {
            "fieldname": "date",
            "label": "Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),  // Set default to today's date
            "reqd": 1  // Make it a required field
        }
    ]
};
