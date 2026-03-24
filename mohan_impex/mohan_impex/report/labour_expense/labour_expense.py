import frappe
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": "Type", "fieldname": "type", "fieldtype": "Data", "width": 120},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Reference", "fieldname": "reference", "fieldtype": "Dynamic Link", "options": "reference_doctype", "width": 150},
        {"label": "Party", "fieldname": "party", "fieldtype": "Link", "options": "Supplier", "width": 180},
        {"label": "Supplier/Customer", "fieldname": "party_link", "fieldtype": "Data", "width": 180},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 120},
        {"label": "Cost Center", "fieldname": "cost_center", "fieldtype": "Link", "options": "Cost Center", "width": 150},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):

    result = []

    base_filters = {
        # "docstatus": 1,
        "custom_total_labour_cost": (">", 0),
        "contractors_name": ["is", "set"]
    }

    # 🔹 Date filter
    if filters.get("from_date") and filters.get("to_date"):
        from_date = getdate(filters.get("from_date"))
        to_date = getdate(filters.get("to_date"))

        if to_date < from_date:
            frappe.throw("To Date cannot be before From Date")

        base_filters["posting_date"] = ["between", [from_date, to_date]]

    # 🔹 Optional filters
    if filters.get("warehouse"):
        base_filters["set_warehouse"] = filters.get("warehouse")

    if filters.get("branch"):
        base_filters["branches"] = filters.get("branch")

    if filters.get("cost_center"):
        base_filters["cost_center"] = filters.get("cost_center")

    if filters.get("party"):
        base_filters["contractors_name"] = filters.get("party")

    type_filter = filters.get("type")

    # ================= UNLOADING =================
    if type_filter in (None, "", "Unloading"):

        pr_filters = base_filters.copy()

        pr_data = frappe.db.get_all(
            "Purchase Receipt",
            fields=[
                "posting_date",
                "contractors_name",
                "supplier",
                "name",
                "set_warehouse",
                "branches",
                "cost_center",
                "total_qty",
                "custom_total_labour_cost"
            ],
            filters=pr_filters,
            order_by="posting_date desc"
        )

        for row in pr_data:
            result.append({
                "type": "Unloading",
                "reference_doctype": "Purchase Receipt",
                "date": row.posting_date,
                "reference": row.name,
                "party": row.contractors_name,
                "party_link": row.supplier,
                "warehouse": row.set_warehouse,
                "branch": row.branches,
                "cost_center": row.cost_center,
                "qty": row.total_qty,
                "amount": row.custom_total_labour_cost
            })

    # ================= LOADING =================
    if type_filter in (None, "", "Loading"):

        dn_filters = base_filters.copy()

        dn_data = frappe.db.get_all(
            "Delivery Note",
            fields=[
                "posting_date",
                "contractors_name",
                "customer",
                "name",
                "set_warehouse",
                "branches",
                "cost_center",
                "total_qty",
                "custom_total_labour_cost"
            ],
            filters=dn_filters,
            order_by="posting_date desc"
        )

        for row in dn_data:
            result.append({
                "type": "Loading",
                "reference_doctype": "Delivery Note",
                "date": row.posting_date,
                "reference": row.name,
                "party": row.contractors_name,
                "party_link": row.customer,
                "warehouse": row.set_warehouse,
                "branch": row.branches,
                "cost_center": row.cost_center,
                "qty": row.total_qty,
                "amount": row.custom_total_labour_cost
            })

    # 🔹 Final sorting (combined)
    result.sort(key=lambda x: x.get("date") or "", reverse=True)

    return result