import frappe

@frappe.whitelist()
def get_employee_leaves(employee=None, department=None, start_date=None, end_date=None):
    """
    Fetches employee leave details for API access.
    Optional filters: employee, department, start_date, end_date.
    """
    conditions = []
    query_filters = {}

    if employee:
        conditions.append("e.employee = %(employee)s")
        query_filters["employee"] = employee

    if department:
        conditions.append("e.department = %(department)s")
        query_filters["department"] = department

    if start_date:
        conditions.append("la.from_date >= %(start_date)s")
        query_filters["start_date"] = start_date

    if end_date:
        conditions.append("la.to_date <= %(end_date)s")
        query_filters["end_date"] = end_date

    where_clause = " AND ".join(conditions)
    where_clause = f"WHERE {where_clause}" if where_clause else ""

    data = frappe.db.sql(f"""
        SELECT 
            e.employee, e.employee_name, e.department, e.branch,
            la.leave_type, la.from_date, la.to_date,
            DATEDIFF(la.to_date, la.from_date) + 1 AS total_leave_days
        FROM `tabEmployee` e
        LEFT JOIN `tabLeave Application` la ON e.employee = la.employee
        {where_clause}
    """, query_filters, as_dict=True)

    return data
