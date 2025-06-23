# leave_balance_summary.py

import frappe
from hrms.api import get_leave_balance_map

def execute(filters=None):
    columns = [
        {"label": "Leave Type", "fieldname": "leave_type", "fieldtype": "Data", "width": 200},
        {"label": "Allocated", "fieldname": "allocated", "fieldtype": "Float", "width": 100},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Float", "width": 100},
    ]
    
    employee = filters.get("employee") if filters else None
    if not employee:
        return columns, []

    leave_balance = get_leave_balance_map(employee)
    
    data = []
    for leave_type, values in leave_balance.items():
        data.append({
            "leave_type": leave_type,
            "allocated": values.get("allocated_leaves", 0),
            "balance": values.get("balance_leaves", 0),
        })

    return columns, data
