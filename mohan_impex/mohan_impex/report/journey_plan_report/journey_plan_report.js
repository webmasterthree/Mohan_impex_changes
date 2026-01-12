// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.query_reports["Journey Plan Report"] = {
    "filters": [
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
        },
		{
            "fieldname": "area",
            "label": __("Area"),
            "fieldtype": "Link",
            "options": "Territory",
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_end(),
        }
    ],
    // onload: function () {
	// 	// 🔹 Legend
	// 	frappe.msgprint({
	// 		title: "Legend",
	// 		indicator: "blue",
	// 		message: `
	// 			<div>
	// 				<p><span style="color:green;font-weight:bold">● Green</span> : Planned & Visited</p>
	// 				<p><span style="color:red;font-weight:bold">● Red</span> : Planned but Not Visited</p>
	// 				<p><span style="color:blue;font-weight:bold">● Blue</span> : Unplanned Visit</p>
	// 			</div>
	// 		`
	// 	});
	// },

	// formatter: function (value, row, column, data, default_formatter) {
	// 	value = default_formatter(value, row, column, data);

	// 	if (column.fieldname === "customer" && data && data.match_status) {

	// 		if (data.match_status === "green") {
	// 			value = `<span style="color:green;font-weight:bold">${value}</span>`;
	// 		}
	// 		else if (data.match_status === "red") {
	// 			value = `<span style="color:red;font-weight:bold">${value}</span>`;
	// 		}
	// 		else if (data.match_status === "blue") {
	// 			value = `<span style="color:blue;font-weight:bold">${value}</span>`;
	// 		}
	// 	}
	// 	return value;
	// }
};
