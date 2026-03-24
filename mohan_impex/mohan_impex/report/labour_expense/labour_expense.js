frappe.query_reports["Labour Expense"] = {
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
			fieldname: "type",
			label: "Type",
			fieldtype: "Select",
			options: "\nLoading\nUnloading"
		},
		{
			fieldname: "party",
			label: "Contractor",
			fieldtype: "Link",
			options: "Supplier",
			get_query: function () {
				return {
					filters: {
						"supplier_group": "Labour Supply Contractor"
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