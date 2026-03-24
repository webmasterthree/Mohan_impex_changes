import frappe
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Reference", "fieldname": "reference", "fieldtype": "Dynamic Link", "options": "reference_doctype", "width": 150},
        {"label": "Transporter", "fieldname": "party", "fieldtype": "Link", "options": "Supplier", "width": 180},
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
        "transport_charges": (">", 0),
        "transporter": ["!=", ""]
    }

    # 🔹 Date filter
    if filters.get("from_date") or filters.get("to_date"):
        if not (filters.get("from_date") and filters.get("to_date")):
            frappe.throw("Both From Date and To Date are required")

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
        base_filters["transporter"] = filters.get("party")

    # ================= PURCHASE RECEIPT =================
    pr_data = frappe.db.get_all(
        "Purchase Receipt",
        fields=[
            "posting_date",
            "transporter",
            "supplier",
            "name",
            "set_warehouse",
            "branches",
            "cost_center",
            "total_qty",
            "transport_charges"
        ],
        filters=base_filters,
        order_by="posting_date desc"
    )

    for row in pr_data:
        result.append({
            "reference_doctype": "Purchase Receipt",
            "date": row.posting_date,
            "reference": row.name,
            "party": row.transporter,
            "party_link": row.supplier,
            "warehouse": row.set_warehouse,
            "branch": row.branches,
            "cost_center": row.cost_center,
            "qty": row.total_qty,
            "amount": row.transport_charges
        })

    # ================= DELIVERY NOTE =================
    dn_filters = base_filters.copy()
    dn_filters.pop("transport_charges", None)  # remove PR-specific filter
    dn_filters["custom_transport_charges"] = (">", 0)

    dn_data = frappe.db.get_all(
        "Delivery Note",
        fields=[
            "posting_date",
            "transporter",
            "customer",
            "name",
            "set_warehouse",
            "branches",
            "cost_center",
            "total_qty",
            "custom_transport_charges"
        ],
        filters=dn_filters,
        order_by="posting_date desc"
    )

    for row in dn_data:
        result.append({
            "reference_doctype": "Delivery Note",
            "date": row.posting_date,
            "reference": row.name,
            "party": row.transporter,
            "party_link": row.customer,
            "warehouse": row.set_warehouse,
            "branch": row.branches,
            "cost_center": row.cost_center,
            "qty": row.total_qty,
            "amount": row.custom_transport_charges
        })

    # 🔹 Final sorting
    result.sort(key=lambda x: x.get("date") or "", reverse=True)

    return result