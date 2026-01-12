# Copyright (c) 2026, Edubild and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Employee ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Journey Plan"),
            "fieldname": "journey_plan",
            "fieldtype": "Link",
            "options": "Journey Plan",
            "width": 150
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("Visit Date"),
            "fieldname": "visit_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Area"),
            "fieldname": "area",
            "fieldtype": "Link",
            "options": "Territory",
            "width": 150
        }
        # {
        #     "label": _("Customer Visit Management"),
        #     "fieldname": "cvm_id",
        #     "fieldtype": "Link",
        #     "options": "Customer Visit Management",
        #     "width": 150
        # }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    query = f"""
        SELECT 
            emp.name AS employee,
            emp.employee_name,
            jp.name AS journey_plan,
            jp.visit_date,
            jp.area,
            cvm.name AS cvm_id,
            cvm.customer AS cvm_customer,
            DATE(cvm.creation) AS cvm_date,
            trp.primary_customer,
            trp.secondary_customer
        FROM `tabEmployee` emp
        LEFT JOIN `tabJourney Plan` jp
            ON emp.name = jp.created_by_emp
        LEFT JOIN `tabTrips` trp
            ON jp.name = trp.parent
        LEFT JOIN `tabCustomer Visit Management` cvm
            ON emp.name = cvm.created_by_emp
            AND DATE(jp.visit_date) = DATE(cvm.creation)
        WHERE
            jp.visit_date BETWEEN %(from_date)s AND %(to_date)s
            {conditions}
        ORDER BY emp.name, jp.visit_date
    """
    
    rows = frappe.db.sql(query, filters, as_dict=True)
    
    # Create a dictionary to organize data by employee and date
    employee_data = {}
    
    for row in rows:
        key = (row.get("employee"), row.get("visit_date"))
        
        if key not in employee_data:
            employee_data[key] = {
                "employee": row.get("employee"),
                "employee_name": row.get("employee_name"),
                "visit_date": row.get("visit_date"),
                "journey_plan": row.get("journey_plan"),
                "area": row.get("area"),
                "jp_customers": set(),
                "cvm_customers": set(),
                "cvm_id": row.get("cvm_id")
            }
        
        # Collect JP customers
        if row.get("primary_customer"):
            employee_data[key]["jp_customers"].update(
                cust.strip() for cust in row["primary_customer"].split(",") if cust.strip()
            )
        
        if row.get("secondary_customer"):
            employee_data[key]["jp_customers"].update(
                cust.strip() for cust in row["secondary_customer"].split(",") if cust.strip()
            )
        
        # Collect CVM customers
        if row.get("cvm_customer"):
            employee_data[key]["cvm_customers"].update(
                cust.strip() for cust in row["cvm_customer"].split(",") if cust.strip()
            )
    
    final_data = []
    
    for key, data_dict in employee_data.items():
        employee = data_dict["employee"]
        employee_name = data_dict["employee_name"]
        journey_plan = data_dict["journey_plan"]
        visit_date = data_dict["visit_date"]
        area = data_dict["area"]
        cvm_id = data_dict["cvm_id"]
        
        jp_customers = sorted(data_dict["jp_customers"])
        cvm_customers = data_dict["cvm_customers"]
        
        # Header row
        final_data.append({
            "name": employee,
            "employee_name": employee_name,
            "journey_plan": journey_plan,
            "visit_date": visit_date,
            "area": area,
            "cvm_id": cvm_id,
            "customer": ""
        })
        
        # JP customers (green or red)
        for customer in jp_customers:
            # Check if customer exists in CVM
            if customer in cvm_customers:
                # GREEN: Customer exists in both JP and CVM
                html_customer = f'''
                <div style="
                    background-color: #d4edda;
                    color: #155724;
                    padding: 5px;
                    border-radius: 4px;
                    text-align: center;
                    margin: 2px 0;
                ">
                    {customer}
                </div>
                '''
            else:
                # RED: Customer in JP but not in CVM
                html_customer = f'''
                <div style="
                    background-color: #f8d7da;
                    color: #721c24;
                    padding: 5px;
                    border-radius: 4px;
                    text-align: center;
                    margin: 2px 0;
                ">
                    {customer}
                </div>
                '''
            
            final_data.append({
                "name": "",
                "employee_name": "",
                "journey_plan": "",
                "visit_date": "",
                "area": "",
                "cvm_id": "",
                "customer": html_customer
            })
        
        # CVM only customers (blue)
        # Find customers that are in CVM but not in JP
        cvm_only_customers = sorted(cvm_customers - set(jp_customers))
        
        for customer in cvm_only_customers:
            # BLUE: Customer in CVM but not in JP
            html_customer = f'''
            <div style="
                background-color: #E6E6FA;
                color: #4B0082;
                padding: 5px;
                border-radius: 4px;
                text-align: center;
                margin: 2px 0;
            ">
                {customer}
            </div>
            '''
            
            final_data.append({
                "name": "",
                "employee_name": "",
                "journey_plan": "",
                "visit_date": "",
                "area": "",
                "cvm_id": "",
                "customer": html_customer
            })
    
    return final_data

def get_conditions(filters):
    conditions = ""
    
    if filters.get("employee"):
        if isinstance(filters.get("employee"), str):
            filters["employee"] = (filters["employee"],)
        conditions += " AND emp.name IN %(employee)s"
    
    if filters.get("area"):
        if isinstance(filters.get("area"), str):
            filters["area"] = (filters["area"],)
        conditions += " AND jp.area IN %(area)s"
    
    return conditions
