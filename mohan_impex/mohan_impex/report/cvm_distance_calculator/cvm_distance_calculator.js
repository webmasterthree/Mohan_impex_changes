// Copyright (c) 2026, Edubild and contributors
// For license information, please see license.txt

frappe.query_reports["CVM Distance Calculator"] = {
	filters: [
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
		}
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "employee_id" && data?.employee_id) {
			return `
				<div style="display:flex; gap:8px; align-items:center;">
					<a href="javascript:void(0)"
					style="color:#1a73e8; font-weight:600; text-decoration: underline;"
					onclick="frappe.query_reports['CVM Distance Calculator'].open_route(
						'${data.employee_id}', 
						'${data.work_date}',  // Pass work_date
						'${data.employee_checkin}'
					)">
						${data.employee_id}
					</a>
					<span
						title="Show CVM Route"
						style="cursor:pointer; color:#28a745; font-size:14px;"
						onclick="frappe.query_reports['CVM Distance Calculator'].open_route(
							'${data.employee_id}',
							'${data.work_date}',  // Pass work_date
							'${data.employee_checkin}'
						)">
						🗺️
					</span>
				</div>
			`;
		}

		return value;
	},

	open_route: function (employee, work_date, checkin) {
		let filters = frappe.query_report.get_filter_values();
		
		frappe.call({
			method: "mohan_impex.mohan_impex.report.cvm_distance_calculator.cvm_distance_calculator.get_employee_route",
			args: {
				employee: employee,
				from_date: filters.from_date,
				to_date: filters.to_date,
				work_date: work_date  // Pass specific work_date
			},
			callback: function (r) {
				let points = r.message || [];
				
				if (points.length < 2) {
					frappe.msgprint("Route ke liye minimum 2 locations chahiye");
					return;
				}

				let origin = points[0];
				let destination = points[points.length - 1];
				let waypoints = points.slice(1, -1);

				let url =
					"https://www.google.com/maps/dir/?api=1" +
					"&origin=" + origin +
					"&destination=" + destination +
					(waypoints.length ? "&waypoints=" + waypoints.join("|") : "") +
					"&travelmode=driving";

				window.open(url, "_blank");
			}
		});
	}

};


/* -------------------------------------------------------
   OPEN ROUTE (Exact technique you shared)
------------------------------------------------------- */

// frappe.query_reports["CVM Distance Calculator"].open_route = function (employee) {

//     let filters = frappe.query_report.get_filter_values();

//     frappe.call({
//         method: "mohan_impex.mohan_impex.report.cvm_distance_calculator.cvm_distance_calculator.get_employee_route",
//         args: {
//             employee: employee,
//             from_date: filters.from_date,
//             to_date: filters.to_date
//         },
//         callback: function (r) {
//             let points = r.message || [];

//             if (points.length < 2) {
//                 frappe.msgprint("Route ke liye minimum 2 locations chahiye");
//                 return;
//             }

//             // First = origin, Last = destination, Middle = waypoints
//             let origin = points[0];
//             let destination = points[points.length - 1];
//             let waypoints = points.slice(1, -1);

//             let url =
//                 "https://www.google.com/maps/dir/?api=1" +
//                 "&origin=" + origin +
//                 "&destination=" + destination +
//                 (waypoints.length ? "&waypoints=" + waypoints.join("|") : "") +
//                 "&travelmode=driving";

//             window.open(url, "_blank");
//         }
//     });
// };

