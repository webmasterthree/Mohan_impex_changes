# Copyright (c) 2026, Edubild and contributors
# For license information, please see license.txt


import frappe
from frappe import _
import math


# -------------------------------------------------
# Main Entry Point
# -------------------------------------------------
def execute(filters=None):
	filters = filters or {}

	raw_data = get_raw_data(filters)
	columns, data = build_dynamic_columns_and_data(raw_data)

	return columns, data


# -------------------------------------------------
# Step 1: Fetch Raw Data
# -------------------------------------------------
def get_raw_data(filters):
	return frappe.db.sql(
		"""
		SELECT
			emp.name AS employee_id,
			emp.employee_name,
			DATE(ec_in.time) AS work_date,
			ec_in.name AS employee_checkin,
			ec_out.name AS employee_checkout,
			cvm.customer,
			cvm.latitude,
			cvm.longitude,
			cvm.creation
		FROM `tabEmployee` emp

		LEFT JOIN `tabEmployee Checkin` ec_in
			ON ec_in.employee = emp.name
			AND ec_in.log_type = 'IN'

		LEFT JOIN `tabEmployee Checkin` ec_out
			ON ec_out.employee = emp.name
			AND ec_out.log_type = 'OUT'
			AND DATE(ec_out.time) = DATE(ec_in.time)

		LEFT JOIN `tabCustomer Visit Management` cvm
			ON cvm.created_by_emp = emp.name
			AND DATE(cvm.creation) = DATE(ec_in.time)

		WHERE 1=1
		{conditions}

		ORDER BY emp.name, work_date, cvm.creation
		""".format(
			conditions=get_conditions(filters)
		),
		filters,
		as_dict=True
	)


# -------------------------------------------------
# Step 2: Dynamic Columns + Distance
# -------------------------------------------------
def build_dynamic_columns_and_data(raw):
	grouped = {}
	max_customers = 0

	for r in raw:
		key = (r.employee_id, r.work_date)

		if key not in grouped:
			grouped[key] = {
				"employee_id": r.employee_id,
				"employee_name": r.employee_name,
				"work_date": r.work_date,  # ✅ Add work_date here
				"employee_checkin": r.employee_checkin,
				"employee_checkout": r.employee_checkout,
				"visits": []
			}

		if r.customer and r.latitude and r.longitude:
			grouped[key]["visits"].append({
				"customer": r.customer,
				"lat": float(r.latitude),
				"lon": float(r.longitude),
				"creation": r.creation
			})

		max_customers = max(max_customers, len(grouped[key]["visits"]))

	# ---------------- Columns ----------------
	columns = [
		{"label": _("Employee"), "fieldname": "employee_id", "fieldtype": "Link", "options": "Employee", "width": 120},
		{"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
		{"label": _("Date"), "fieldname": "work_date", "fieldtype": "Date", "width": 100},  # ✅ Add Date column
		{"label": _("Check-in"), "fieldname": "employee_checkin", "fieldtype": "Link", "options": "Employee Checkin", "width": 140},
	]

	for i in range(1, max_customers + 1):
		columns.append({
			"label": _(f"Customer {i}"),
			"fieldname": f"customer_{i}",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 140
		})

	columns.extend([
		{"label": _("Check-out"), "fieldname": "employee_checkout", "fieldtype": "Link", "options": "Employee Checkin", "width": 140},
		{"label": _("Distance KM"), "fieldname": "distance_km", "fieldtype": "Float", "width": 120},
	])

	# ---------------- Data ----------------
	data = []

	for key, g in grouped.items():
		row = {
			"employee_id": g["employee_id"],
			"employee_name": g["employee_name"],
			"work_date": g["work_date"],  # ✅ Important: Add work_date to row
			"employee_checkin": g["employee_checkin"],
			"employee_checkout": g["employee_checkout"],
		}

		coords = []

		for i, visit in enumerate(g["visits"], start=1):
			row[f"customer_{i}"] = visit["customer"]
			coords.append((visit["lat"], visit["lon"]))

		row["distance_km"] = round(calculate_total_distance(coords), 2)

		data.append(row)

	return columns, data


# -------------------------------------------------
# Distance Calculation (Haversine)
# -------------------------------------------------
def calculate_total_distance(coords):
	if len(coords) < 2:
		return 0

	total = 0
	for i in range(len(coords) - 1):
		total += haversine(coords[i], coords[i + 1])

	return total


def haversine(c1, c2):
	lat1, lon1 = c1
	lat2, lon2 = c2

	R = 6371  # Earth radius (KM)

	dlat = math.radians(lat2 - lat1)
	dlon = math.radians(lon2 - lon1)

	a = (
		math.sin(dlat / 2) ** 2
		+ math.cos(math.radians(lat1))
		* math.cos(math.radians(lat2))
		* math.sin(dlon / 2) ** 2
	)

	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	return R * c


# -------------------------------------------------
# Filters
# -------------------------------------------------
def get_conditions(filters):
	conditions = []

	if filters.get("employee"):
		conditions.append(" AND emp.name = %(employee)s")

	if filters.get("from_date"):
		conditions.append(" AND DATE(ec_in.time) >= %(from_date)s")

	if filters.get("to_date"):
		conditions.append(" AND DATE(ec_in.time) <= %(to_date)s")

	return " ".join(conditions)




@frappe.whitelist()
def get_employee_route(employee, from_date, to_date, work_date=None):
    """
    Return ordered lat-long list for CVM visits
    If work_date is provided, only show visits for that specific date
    """
    
    conditions = " AND created_by_emp = %s"
    params = [employee]
    
    if work_date:
        # If specific work_date is provided, show only that day's visits
        conditions += " AND DATE(creation) = %s"
        params.append(work_date)
    else:
        # Otherwise show all visits in date range
        conditions += " AND DATE(creation) BETWEEN %s AND %s"
        params.extend([from_date, to_date])
    
    rows = frappe.db.sql(
        """
        SELECT
            latitude,
            longitude,
            DATE(creation) as visit_date
        FROM `tabCustomer Visit Management`
        WHERE
            latitude IS NOT NULL
            AND longitude IS NOT NULL
            {conditions}
        ORDER BY creation ASC
        """.format(conditions=conditions),
        tuple(params),
        as_dict=True
    )

    # Convert to "lat,lng" format
    points = [f"{r.latitude},{r.longitude}" for r in rows]

    return points