import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import nowdate
from mohan_impex.api import get_signed_token

@frappe.whitelist()
def get_sales_target():
    try:
        emp_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        month = frappe.form_dict.get('month')
        year = frappe.form_dict.get('year')
        if not month or not year:
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Month and year must be provided"
            return
        month_num = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }.get(month)
        if month_num is None:
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Invalid month name"
            return
        sales_person = frappe.get_value("Sales Person", {"employee": emp_id, "enabled": 1}, "name")
        fiscal_year = get_fiscal_year(get_first_date_of_month(year, month_num), as_dict=True).get("name") or ""
        sales_target = get_sales_target_by_sales_invoice(sales_person, fiscal_year, month, year)
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Sales Target has been successfully fetched"
        frappe.local.response['data'] = sales_target
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

def get_sales_target_by_sales_invoice(sales_person, fiscal_year, month, year):
    query = """
        select sii.item_code, sii.item_group, sum(sii.stock_qty) as qty, sum(sii.amount) as amount, td.target_type, round(td.target_qty*(mdp.percentage_allocation/100)) as target_volume, td.target_amount
        from `tabSales Invoice` as si
        join `tabSales Team` as st on st.parent = si.name
        join `tabSales Invoice Item` as sii on sii.parent = si.name
        join `tabTarget Detail` as td on td.item_group = sii.item_group
        join `tabMonthly Distribution Percentage` as mdp on mdp.parent = td.distribution_id and mdp.month = "%s"
        where 
            st.sales_person = "%s" 
            and td.fiscal_year = "%s"
            and MONTHNAME(si.posting_date) = "%s"
        group by sii.item_code, sii.item_group
    """%(month, sales_person, fiscal_year, month)
    sales_targets = frappe.db.sql(query, as_dict=True)
    item_group_targets = {}
    for target in sales_targets:
        if target.item_code not in item_group_targets.get(target.item_group, []):
            item_group_targets.setdefault(target.item_group, []).append({"item_code": target.item_code, "target_type": target.target_type, "qty": 0, "amount": 0, "target_volume": 0, "target_amount": 0, "achieved_percent": 0})
        for item in item_group_targets[target.item_group]:
            if item["item_code"] == target.item_code:
                item["qty"] += target.qty
                item["amount"] += target.amount
                item["target_volume"] = target.target_volume
                item["target_amount"] = target.target_amount
                if target.target_type == "Amount":
                    item["achieved_percent"] = round((target.amount/target.target_amount)*100, 2) if target.target_amount else 0
                else:
                    item["achieved_percent"] = round((target.qty/target.target_volume)*100, 2) if target.target_volume else 0
    for k, v in item_group_targets.items():
        item_group_targets[k] = {
            "item_group": k,
            "items": v,
            "total_qty": sum(item["qty"] for item in v),
            "total_amount": sum(item["amount"] for item in v),
            "target_type": v[0]["target_type"],
            "total_target_volume": v[0]["target_volume"],
            "total_target_amount": v[0]["target_amount"],
        }
        if v[0]["target_type"] != "Volume":
            item_group_targets[k].update({"achieved_percent": round((sum(item["amount"] for item in v) / v[0]["target_amount"])*100, 2) if v[0]["target_amount"] else 0})
        else:
            item_group_targets[k].update({"achieved_percent": round((sum(item["qty"] for item in v) / v[0]["target_volume"])*100, 2) if v[0]["target_volume"] else 0})
    sales_targets = list(item_group_targets.values())
    overall = {"volume": {"percent": 0, "count": 0}, "amount": {"percent": 0, "count": 0}}
    for target in sales_targets:
        overall[target["target_type"].lower()]["percent"] += target["achieved_percent"]
        overall[target["target_type"].lower()]["count"] += 1
    for key in overall:
        overall[key] = round(overall[key]["percent"] / overall[key]["count"], 2) if overall[key]["count"] else 0
        # overall[key].pop("count")
    overall["total"] = round((overall["volume"] + overall["amount"])/2, 2)
    data = {
        "sales_targets": sales_targets,
        "overall_achieved_percent": overall
    }
    return data

from datetime import datetime

def get_first_date_of_month(year, month):
    return datetime(int(year), month, 1)

@frappe.whitelist()
def get_leader_board():
    try:
        fiscal_year = get_fiscal_year(nowdate(), as_dict=True).get("name") or ""
        month = datetime.now().strftime("%B")
        query = """
            select sp.employee, st.sales_person, sii.item_code, sii.item_group, sum(sii.stock_qty) as qty, sum(sii.amount) as amount, td.target_type, round(td.target_qty*(mdp.percentage_allocation/100)) as target_volume, td.target_amount
            from `tabSales Invoice` as si
            join `tabSales Team` as st on st.parent = si.name
            join `tabSales Person` as sp on sp.name = st.sales_person
            join `tabSales Invoice Item` as sii on sii.parent = si.name
            join `tabTarget Detail` as td on td.item_group = sii.item_group
            join `tabMonthly Distribution Percentage` as mdp on mdp.parent = td.distribution_id and mdp.month = "%s"
            where 
                sp.enabled = 1
                and td.fiscal_year = "%s"
                and MONTHNAME(si.posting_date) = "%s"
            group by st.sales_person, sii.item_code, sii.item_group
        """%(month, fiscal_year, month)
        sales_targets = frappe.db.sql(query, as_dict=True)
        sales_person_targets = {}
        for target in sales_targets:
            if target["sales_person"] not in sales_person_targets:
                sales_person_targets[target["sales_person"]] = []
            sales_person_targets[target["sales_person"]].append(target)

        # Now, `sales_person_targets` will contain sales targets segregated by sales person
        # return sales_person_targets
        overall_persons = []
        default_user_image = frappe.get_single("Mohan Impex Settings").default_profile_image
        default_user_image = get_signed_token(default_user_image)
        for sales_person, sales_person_target in sales_person_targets.items():
            item_group_targets = {}
            for target in sales_person_target:
                if target.item_code not in item_group_targets.get(target.item_group, []):
                    item_group_targets.setdefault(target.item_group, []).append({"item_code": target.item_code, "target_type": target.target_type, "qty": 0, "amount": 0, "target_volume": 0, "target_amount": 0, "achieved_percent": 0, "employee": target.employee, "image": default_user_image})
                for item in item_group_targets[target.item_group]:
                    if item["item_code"] == target.item_code:
                        item["sales_person"] = target.sales_person
                        item["qty"] += target.qty
                        item["amount"] += target.amount
                        item["target_volume"] = target.target_volume
                        item["target_amount"] = target.target_amount
                        if target.target_type == "Amount":
                            item["achieved_percent"] = round((target.amount/target.target_amount)*100, 2) if target.target_amount else 0
                        else:
                            item["achieved_percent"] = round((target.qty/target.target_volume)*100, 2) if target.target_volume else 0
            for k, v in item_group_targets.items():
                item_group_targets[k] = {
                    "item_group": k,
                    "items": v,
                    "total_qty": sum(item["qty"] for item in v),
                    "total_amount": sum(item["amount"] for item in v),
                    "target_type": v[0]["target_type"],
                    "total_target_volume": v[0]["target_volume"],
                    "total_target_amount": v[0]["target_amount"],
                    "employee": v[0]["employee"],
                    "image": v[0]["image"]
                }
                if v[0]["target_type"] != "Volume":
                    item_group_targets[k].update({"achieved_percent": round((sum(item["amount"] for item in v) / v[0]["target_amount"])*100, 2) if v[0]["target_amount"] else 0})
                else:
                    item_group_targets[k].update({"achieved_percent": round((sum(item["qty"] for item in v) / v[0]["target_volume"])*100, 2) if v[0]["target_volume"] else 0})
            sales_targets = list(item_group_targets.values())
            percent_calc = {"volume": {"percent": 0, "count": 0}, "amount": {"percent": 0, "count": 0}}
            overall = {}
            for target in sales_targets:
                percent_calc[target["target_type"].lower()]["percent"] += target["achieved_percent"]
                percent_calc[target["target_type"].lower()]["count"] += 1
            for key in percent_calc:
                percent_calc[key] = round(percent_calc[key]["percent"] / percent_calc[key]["count"], 2) if percent_calc[key]["count"] else 0
                # overall[key].pop("count")
            overall["user_image"] = sales_targets[0]["image"]
            overall["total_percent"] = round((percent_calc["volume"] + percent_calc["amount"])/2, 2)
            user_id, employee_name = frappe.get_value("Employee", sales_targets[0]["employee"], ["user_id", "employee_name"])
            user_image = frappe.get_value("User", {"name": user_id}, "user_image")
            overall["session_user"] = False
            if user_id == frappe.session.user: overall["session_user"] = True
            if user_image: overall["image"] = get_signed_token(user_image)
            overall.update({"name": employee_name})
            overall_persons.append(overall)
        overall_persons = sorted(
            overall_persons,
            key=lambda x: (x["total_percent"], x["name"])
        )
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Leadboard fetched successfully"
        frappe.local.response['data'] = overall_persons
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"