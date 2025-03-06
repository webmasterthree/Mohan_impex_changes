# import frappe
# from frappe import _

# def execute(filters=None):
#     if not filters:
#         filters = {}

#     conditions = ""
#     values = []

#     if filters.get("employee"):
#         conditions += " AND ss.employee = %s"
#         values.append(filters["employee"])

#     if filters.get("month") and filters.get("year"):
#         conditions += " AND ss.start_date BETWEEN %s AND %s"
#         values.append(f"{filters['year']}-{filters['month']}-01")
#         values.append(f"{filters['year']}-{filters['month']}-31")

#     # Fetch salary slips
#     salary_slips = frappe.db.sql(f"""
#         SELECT ss.name, ss.employee, ss.employee_name, ss.department, ss.designation, ss.branch, 
#                ss.custom_pan, ss.custom_joining_date, ss.total_working_days, ss.gross_pay, ss.total_deduction
#         FROM `tabSalary Slip` ss
#         WHERE 1=1 {conditions}
#         ORDER BY ss.employee_name
#     """, tuple(values), as_dict=True)

#     if not salary_slips:
#         return [], []  # Return empty data if no salary slips found

#     # Initialize dictionaries for earnings and deductions
#     earnings_components = set()
#     deductions_components = set()
#     salary_data = {}

#     for slip in salary_slips:
#         salary_data[slip["name"]] = {
#             "employee": slip["employee"],
#             "employee_name": slip["employee_name"],
#             "department": slip["department"],
#             "designation": slip["designation"],
#             "branch": slip["branch"],
#             "custom_pan": slip["custom_pan"],
#             "custom_joining_date": slip["custom_joining_date"],
#             "total_working_days": slip["total_working_days"],
#             "gross_pay": slip["gross_pay"],
#             "total_deduction": slip["total_deduction"],
#             "earnings": {},  # Initialize earnings as an empty dictionary
#             "deductions": {}  # Initialize deductions as an empty dictionary
#         }

#     slip_ids = [slip["name"] for slip in salary_slips]

#     # Fetch all earnings in one query
#     earnings = frappe.db.sql("""
#         SELECT parent, salary_component, amount 
#         FROM `tabSalary Detail`
#         WHERE parent IN %(slip_ids)s AND parentfield = 'earnings'
#     """, {"slip_ids": slip_ids}, as_dict=True)

#     # Fetch all deductions in one query
#     deductions = frappe.db.sql("""
#         SELECT parent, salary_component, amount 
#         FROM `tabSalary Detail`
#         WHERE parent IN %(slip_ids)s AND parentfield = 'deductions'
#     """, {"slip_ids": slip_ids}, as_dict=True)

#     # Process earnings and deductions
#     for e in earnings:
#         salary_data[e["parent"]]["earnings"][e["salary_component"]] = e["amount"]
#         earnings_components.add(e["salary_component"])

#     for d in deductions:
#         salary_data[d["parent"]]["deductions"][d["salary_component"]] = d["amount"]
#         deductions_components.add(d["salary_component"])

#     # Define report columns
#     columns = [
#         {"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Data", "width": 120},
#         {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
#         {"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 120},
#         {"label": _("Designation"), "fieldname": "designation", "fieldtype": "Data", "width": 120},
#         {"label": _("Branch"), "fieldname": "branch", "fieldtype": "Data", "width": 120},
#         {"label": _("PAN"), "fieldname": "custom_pan", "fieldtype": "Data", "width": 120},
#         {"label": _("Joining Date"), "fieldname": "custom_joining_date", "fieldtype": "Date", "width": 120},
#         {"label": _("Total Working Days"), "fieldname": "total_working_days", "fieldtype": "Int", "width": 120},
#         {"label": _("Gross Pay"), "fieldname": "gross_pay", "fieldtype": "Currency", "width": 120},
#         {"label": _("Total Deduction"), "fieldname": "total_deduction", "fieldtype": "Currency", "width": 120}
#     ]

#     # Add dynamic earning columns
#     for component in sorted(earnings_components):
#         columns.append({"label": _(component), "fieldname": component, "fieldtype": "Currency", "width": 120})

#     # Add dynamic deduction columns
#     for component in sorted(deductions_components):
#         columns.append({"label": _(component), "fieldname": component, "fieldtype": "Currency", "width": 120})

#     # Process data for report
#     data = []
#     for slip_id, slip in salary_data.items():
#         row = {
#             "employee": slip["employee"],
#             "employee_name": slip["employee_name"],
#             "department": slip["department"],
#             "designation": slip["designation"],
#             "branch": slip["branch"],
#             "custom_pan": slip["custom_pan"],
#             "custom_joining_date": slip["custom_joining_date"],
#             "total_working_days": slip["total_working_days"],
#             "gross_pay": slip["gross_pay"],
#             "total_deduction": slip["total_deduction"]
#         }

#         # Add earnings values
#         for component in earnings_components:
#             row[component] = slip["earnings"].get(component, 0)

#         # Add deductions values
#         for component in deductions_components:
#             row[component] = slip["deductions"].get(component, 0)

#         data.append(row)

#     return columns, data


import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}

    conditions = ""
    values = []

    if filters.get("employee"):
        conditions += " AND ss.employee = %s"
        values.append(filters["employee"])

    if filters.get("month") and filters.get("year"):
        conditions += " AND ss.start_date BETWEEN %s AND %s"
        values.append(f"{filters['year']}-{filters['month']}-01")
        values.append(f"{filters['year']}-{filters['month']}-31")

    # Fetch salary slips with Employee details
    salary_slips = frappe.db.sql(f"""
        SELECT ss.name, ss.employee, ss.employee_name, ss.department, ss.designation, ss.branch, 
               ss.custom_pan, ss.custom_joining_date, ss.total_working_days, ss.gross_pay, ss.total_deduction,
               emp.custom_aadhar_number, emp.provident_fund_account
        FROM `tabSalary Slip` ss
        LEFT JOIN `tabEmployee` emp ON ss.employee = emp.name
        WHERE 1=1 {conditions}
        ORDER BY ss.employee_name
    """, tuple(values), as_dict=True)

    if not salary_slips:
        return [], []  # Return empty data if no salary slips found

    # Initialize dictionaries for earnings and deductions
    earnings_components = set()
    deductions_components = set()
    salary_data = {}

    for slip in salary_slips:
        salary_data[slip["name"]] = {
            "employee": slip["employee"],
            "employee_name": slip["employee_name"],
            "department": slip["department"],
            "designation": slip["designation"],
            "branch": slip["branch"],
            "custom_pan": slip["custom_pan"],
            "custom_aadhar_number": slip["custom_aadhar_number"],
            "provident_fund_account": slip["provident_fund_account"],
            "custom_joining_date": slip["custom_joining_date"],
            "total_working_days": slip["total_working_days"],
            "gross_pay": slip["gross_pay"],
            "total_deduction": slip["total_deduction"],
            "earnings": {},  # Initialize earnings as an empty dictionary
            "deductions": {}  # Initialize deductions as an empty dictionary
        }

    slip_ids = [slip["name"] for slip in salary_slips]

    # Fetch all earnings in one query
    earnings = frappe.db.sql("""
        SELECT parent, salary_component, amount 
        FROM `tabSalary Detail`
        WHERE parent IN %(slip_ids)s AND parentfield = 'earnings'
    """, {"slip_ids": slip_ids}, as_dict=True)

    # Fetch all deductions in one query
    deductions = frappe.db.sql("""
        SELECT parent, salary_component, amount 
        FROM `tabSalary Detail`
        WHERE parent IN %(slip_ids)s AND parentfield = 'deductions'
    """, {"slip_ids": slip_ids}, as_dict=True)

    # Process earnings and deductions
    for e in earnings:
        salary_data[e["parent"]]["earnings"][e["salary_component"]] = e["amount"]
        earnings_components.add(e["salary_component"])

    for d in deductions:
        salary_data[d["parent"]]["deductions"][d["salary_component"]] = d["amount"]
        deductions_components.add(d["salary_component"])

    # Define report columns
    columns = [
        {"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Data", "width": 120},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 120},
        {"label": _("Designation"), "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": _("Branch"), "fieldname": "branch", "fieldtype": "Data", "width": 120},
        {"label": _("PAN"), "fieldname": "custom_pan", "fieldtype": "Data", "width": 120},
        {"label": _("Aadhar Number"), "fieldname": "custom_aadhar_number", "fieldtype": "Data", "width": 150},
        {"label": _("Provident Fund Account"), "fieldname": "provident_fund_account", "fieldtype": "Data", "width": 150},
        {"label": _("Joining Date"), "fieldname": "custom_joining_date", "fieldtype": "Date", "width": 120},
        {"label": _("Total Working Days"), "fieldname": "total_working_days", "fieldtype": "Int", "width": 120},
        {"label": _("Gross Pay"), "fieldname": "gross_pay", "fieldtype": "Currency", "width": 120},
        {"label": _("Total Deduction"), "fieldname": "total_deduction", "fieldtype": "Currency", "width": 120}
    ]

    # Add dynamic earning columns
    for component in sorted(earnings_components):
        columns.append({"label": _(component), "fieldname": component, "fieldtype": "Currency", "width": 120})

    # Add dynamic deduction columns
    for component in sorted(deductions_components):
        columns.append({"label": _(component), "fieldname": component, "fieldtype": "Currency", "width": 120})

    # Process data for report
    data = []
    for slip_id, slip in salary_data.items():
        row = {
            "employee": slip["employee"],
            "employee_name": slip["employee_name"],
            "department": slip["department"],
            "designation": slip["designation"],
            "branch": slip["branch"],
            "custom_pan": slip["custom_pan"],
            "custom_aadhar_number": slip["custom_aadhar_number"],
            "provident_fund_account": slip["provident_fund_account"],
            "custom_joining_date": slip["custom_joining_date"],
            "total_working_days": slip["total_working_days"],
            "gross_pay": slip["gross_pay"],
            "total_deduction": slip["total_deduction"]
        }

        # Add earnings values
        for component in earnings_components:
            row[component] = slip["earnings"].get(component, 0)

        # Add deductions values
        for component in deductions_components:
            row[component] = slip["deductions"].get(component, 0)

        data.append(row)

    return columns, data
