// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.query_reports["Transporter Expense"] = {
	filters: [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.month_start()
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			default: frappe.datetime.month_end()
		},
		{
			fieldname: "party",
			label: "Contractor",
			fieldtype: "Link",
			options: "Supplier",
			get_query: function () {
				return {
					filters: {
						"is_transporter": "1"
					}
				};
			}
		},
		{
			fieldname: "warehouse",
			label: "Warehouse",
			fieldtype: "Link",
			options: "Warehouse"
		},
		{
			fieldname: "branch",
			label: "Branch",
			fieldtype: "Link",
			options: "Branch"
		},
		{
			fieldname: "cost_center",
			label: "Cost Center",
			fieldtype: "Link",
			options: "Cost Center"
		}
	]
};