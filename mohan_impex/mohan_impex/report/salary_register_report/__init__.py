# import frappe
# from frappe import _

# @frappe.whitelist(allow_guest=False)  # Restrict to logged-in users
# def get_salary_slips(employee=None, month=None, year=None):
#     """Fetch Salary Slips with Earnings and Deductions"""
    
#     # Validate month and year
#     if month and (not month.isdigit() or int(month) not in range(1, 13)):
#         return {"status": "error", "message": _("Invalid month. It should be between 1 and 12.")}

#     if year and not year.isdigit():
#         return {"status": "error", "message": _("Invalid year. It should be a number.")}

#     filters = {}
#     if employee:
#         filters["employee"] = employee
#     if month and year:
#         filters["start_date"] = ["between", [f"{year}-{month}-01", f"{year}-{month}-31"]]

#     # Fetch salary slips
#     salary_slips = frappe.get_list(
#         "Salary Slip",
#         filters=filters,
#         fields=[
#             "name", "employee", "employee_name", "department", "designation", "branch",
#             "custom_pan", "custom_joining_date", "total_working_days", "gross_pay", "total_deduction"
#         ]
#     )

#     if not salary_slips:
#         return {"status": "error", "message": _("No salary slips found for the given filters.")}

#     # Collect all salary slip IDs to fetch earnings and deductions in bulk
#     slip_ids = [slip["name"] for slip in salary_slips]

#     # Fetch earnings in one query
#     earnings = frappe.db.sql("""
#         SELECT parent, salary_component, amount FROM `tabSalary Detail`
#         WHERE parent IN %(slip_ids)s AND parentfield = 'earnings'
#     """, {"slip_ids": slip_ids}, as_dict=True)

#     # Fetch deductions in one query
#     deductions = frappe.db.sql("""
#         SELECT parent, salary_component, amount FROM `tabSalary Detail`
#         WHERE parent IN %(slip_ids)s AND parentfield = 'deductions'
#     """, {"slip_ids": slip_ids}, as_dict=True)

#     # Organize earnings and deductions into dictionaries
#     earnings_map = {}
#     deductions_map = {}

#     for entry in earnings:
#         earnings_map.setdefault(entry["parent"], []).append({
#             "salary_component": entry["salary_component"],
#             "amount": entry["amount"]
#         })

#     for entry in deductions:
#         deductions_map.setdefault(entry["parent"], []).append({
#             "salary_component": entry["salary_component"],
#             "amount": entry["amount"]
#         })

#     # Attach earnings and deductions to each salary slip
#     for slip in salary_slips:
#         slip["earnings"] = earnings_map.get(slip["name"], [])
#         slip["deductions"] = deductions_map.get(slip["name"], [])

#     return {"status": "success", "data": salary_slips}


import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)  # Restrict to logged-in users
def get_salary_slips(employee=None, month=None, year=None):
    """Fetch Salary Slips with Earnings, Deductions, Aadhar, and PF Details"""
    
    # Validate month and year
    if month and (not month.isdigit() or int(month) not in range(1, 13)):
        return {"status": "error", "message": _("Invalid month. It should be between 1 and 12.")}

    if year and not year.isdigit():
        return {"status": "error", "message": _("Invalid year. It should be a number.")}

    conditions = ""
    values = []

    if employee:
        conditions += " AND ss.employee = %s"
        values.append(employee)

    if month and year:
        conditions += " AND ss.start_date BETWEEN %s AND %s"
        values.append(f"{year}-{month}-01")
        values.append(f"{year}-{month}-31")

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
        return {"status": "error", "message": _("No salary slips found for the given filters.")}

    # Collect all salary slip IDs to fetch earnings and deductions in bulk
    slip_ids = [slip["name"] for slip in salary_slips]

    # Fetch earnings in one query
    earnings = frappe.db.sql("""
        SELECT parent, salary_component, amount FROM `tabSalary Detail`
        WHERE parent IN %(slip_ids)s AND parentfield = 'earnings'
    """, {"slip_ids": slip_ids}, as_dict=True)

    # Fetch deductions in one query
    deductions = frappe.db.sql("""
        SELECT parent, salary_component, amount FROM `tabSalary Detail`
        WHERE parent IN %(slip_ids)s AND parentfield = 'deductions'
    """, {"slip_ids": slip_ids}, as_dict=True)

    # Organize earnings and deductions into dictionaries
    earnings_map = {}
    deductions_map = {}

    for entry in earnings:
        earnings_map.setdefault(entry["parent"], []).append({
            "salary_component": entry["salary_component"],
            "amount": entry["amount"]
        })

    for entry in deductions:
        deductions_map.setdefault(entry["parent"], []).append({
            "salary_component": entry["salary_component"],
            "amount": entry["amount"]
        })

    # Attach earnings, deductions, Aadhar, and PF details to each salary slip
    for slip in salary_slips:
        slip["earnings"] = earnings_map.get(slip["name"], [])
        slip["deductions"] = deductions_map.get(slip["name"], [])
        slip["custom_aadhar_number"] = slip.get("custom_aadhar_number", "N/A")
        slip["provident_fund_account"] = slip.get("provident_fund_account", "N/A")

    return {"status": "success", "data": salary_slips}
