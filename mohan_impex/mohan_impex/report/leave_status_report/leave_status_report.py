# import frappe

# def execute(filters=None):
#     """
#     Fetches employee leave data for the report.
#     Optional filters: start_date, end_date.
#     """
#     columns = get_columns()
#     data = get_employee_leaves(filters)
    
#     return columns, data

# def get_columns():
#     """
#     Defines the report columns.
#     """
#     return [
#         {"fieldname": "employee", "label": "Employee ID", "fieldtype": "Data", "width": 120},
#         {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
#         {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 120},
#         {"fieldname": "branch", "label": "Location", "fieldtype": "Data", "width": 120},
#         {"fieldname": "custom_reports_one_name", "label": "Report One", "fieldtype": "Data", "width": 150},
#         {"fieldname": "custom_reports_two_name", "label": "Report Two", "fieldtype": "Data", "width": 150},
#         {"fieldname": "leave_type", "label": "Leave Type", "fieldtype": "Data", "width": 120},
#         {"fieldname": "from_date", "label": "From Date", "fieldtype": "Date", "width": 100},
#         {"fieldname": "to_date", "label": "To Date", "fieldtype": "Date", "width": 100},
#         {"fieldname": "total_leave_days", "label": "Total Leave Days", "fieldtype": "Int", "width": 120},
#         {
#             "fieldname": "status", "label": "Leave Status", "fieldtype": "Data", "width": 120,
#             "indicator": "red"  # Default color, will be updated dynamically
#         }
#     ]

# def get_employee_leaves(filters):
#     """
#     Retrieves leave data based on filters, including leave status.
#     Assigns colors to the leave status dynamically.
#     """
#     conditions = []
#     query_filters = {}

#     if filters.get("start_date"):
#         conditions.append("la.from_date >= %(start_date)s")
#         query_filters["start_date"] = filters["start_date"]

#     if filters.get("end_date"):
#         conditions.append("la.to_date <= %(end_date)s")
#         query_filters["end_date"] = filters["end_date"]

#     where_clause = " AND ".join(conditions)
#     where_clause = f"WHERE {where_clause}" if where_clause else ""

#     data = frappe.db.sql(f"""
#         SELECT 
#             e.employee, e.employee_name, e.department, e.branch,
#             e.custom_reports_one_name, e.custom_reports_two_name,
#             la.leave_type, la.from_date, la.to_date, la.status,
#             DATEDIFF(la.to_date, la.from_date) + 1 AS total_leave_days
#         FROM `tabEmployee` e
#         LEFT JOIN `tabLeave Application` la ON e.employee = la.employee
#         {where_clause}
#     """, query_filters, as_dict=True)

#     # Assign colors based on leave status
#     for row in data:
#         if row["status"] == "Approved":
#             row["indicator"] = "green"
#         elif row["status"] == "Rejected":
#             row["indicator"] = "red"
#         elif row["status"] == "Open":
#             row["indicator"] = "orange"
#         else:
#             row["indicator"] = "gray"  # Default color for unknown statuses

#     return data

import frappe

def execute(filters=None):
    """
    Fetches employee leave data for the report.
    Optional filters: start_date, end_date.
    """
    columns = get_columns()
    data = get_employee_leaves(filters)
    
    return columns, data

def get_columns():
    """
    Defines the report columns.
    """
    return [
        {"fieldname": "employee", "label": "Employee ID", "fieldtype": "Data", "width": 120},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 120},
        {"fieldname": "branch", "label": "Location", "fieldtype": "Data", "width": 120},
        {"fieldname": "custom_reports_one_name", "label": "Report One", "fieldtype": "Data", "width": 150},
        {"fieldname": "custom_reports_two_name", "label": "Report Two", "fieldtype": "Data", "width": 150},
        {"fieldname": "leave_type", "label": "Leave Type", "fieldtype": "Data", "width": 120},
        {"fieldname": "from_date", "label": "From Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "to_date", "label": "To Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "total_leave_days", "label": "Total Leave Days", "fieldtype": "Int", "width": 120},
        {
            "fieldname": "status", "label": "Leave Status", "fieldtype": "Data", "width": 120
        },
        {
            "fieldname": "status_indicator", "label": "Status Indicator", "fieldtype": "Data", "width": 100, "hidden": 1
        }
    ]

def get_employee_leaves(filters):
    """
    Retrieves leave data based on filters, including leave status.
    Assigns colors to the leave status dynamically.
    """
    conditions = []
    query_filters = {}

    if filters.get("start_date"):
        conditions.append("la.from_date >= %(start_date)s")
        query_filters["start_date"] = filters["start_date"]

    if filters.get("end_date"):
        conditions.append("la.to_date <= %(end_date)s")
        query_filters["end_date"] = filters["end_date"]

    where_clause = " AND ".join(conditions)
    where_clause = f"WHERE {where_clause}" if where_clause else ""

    data = frappe.db.sql(f"""
        SELECT 
            e.employee, e.employee_name, e.department, e.branch,
            e.custom_reports_one_name, e.custom_reports_two_name,
            la.leave_type, la.from_date, la.to_date, la.status,
            DATEDIFF(la.to_date, la.from_date) + 1 AS total_leave_days,
            CASE 
                WHEN la.status = 'Approved' THEN 'green'
                WHEN la.status = 'Rejected' THEN 'red'
                WHEN la.status = 'Open' THEN 'orange'
                ELSE 'gray'
            END AS status_indicator
        FROM `tabEmployee` e
        LEFT JOIN `tabLeave Application` la ON e.employee = la.employee
        {where_clause}
    """, query_filters, as_dict=True)

    return data
