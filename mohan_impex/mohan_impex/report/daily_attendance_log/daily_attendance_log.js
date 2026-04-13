// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

// frappe.query_reports["Daily Attendance Log"] = {
// 	"filters": [
// 		{
// 			"fieldname": "from_date",
// 			"label": "From Date",
// 			"fieldtype": "Date",
// 			"reqd": 1
// 		},
// 		{
// 			"fieldname": "to_date",
// 			"label": "To Date",
// 			"fieldtype": "Date",
// 			"reqd": 1
// 		},
// 		{
// 			"fieldname": "employee",
// 			"label": "Employee",
// 			"fieldtype": "Link",
// 			"options": "Employee"
// 		}
// 	]
// };


// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Attendance Log"] = {

    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        }
    ],

    formatter: function(value, row, column, data, default_formatter) {

        value = default_formatter(value, row, column, data);

        // 🔥 Color coding only for Status row
        if (data && data.employee === "Status") {

            if (value === "Absent") {
                value = `<span style="color:red;font-weight:bold">${value}</span>`;
            }
            else if (value === "Present") {
                value = `<span style="color:green;font-weight:bold">${value}</span>`;
            }
            else if (value === "Holiday" || value === "Weekly Off") {
                value = `<span style="color:blue;font-weight:bold">${value}</span>`;
            }
            else if (value === "On Leave") {
                value = `<span style="color:orange;font-weight:bold">${value}</span>`;
            }
            else if (value === "Compensatory Work") {
                value = `<span style="color:purple;font-weight:bold">${value}</span>`;
            }
        }

        return value;
    }
};