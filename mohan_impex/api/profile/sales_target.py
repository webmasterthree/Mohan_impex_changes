import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import nowdate
from mohan_impex.api import get_signed_token, get_exception

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
        get_exception(err)

def get_sales_target_by_sales_invoice(sales_person, fiscal_year, month, year):
    uom = frappe.get_single("Stock Settings").stock_uom or "Kgs"
    
    currency = frappe.get_value("Company", frappe.defaults.get_user_default("Company"), "default_currency")
    currency_symbol = frappe.get_value("Currency", currency, "symbol")

    # query = """
    #     select sii.item_code, sii.item_group, sum(sii.stock_qty) as qty, sum(sii.amount) as amount, td.target_type, round(td.target_qty*(mdp.percentage_allocation/100)) as target_volume, td.target_amount
    #     from `tabSales Invoice` as si
    #     left join `tabSales Team` as st on st.parent = si.name
    #     left join `tabSales Invoice Item` as sii on sii.parent = si.name
    #     left join `tabTarget Detail` as td on td.item_group = sii.item_group
    #     left join `tabMonthly Distribution Percentage` as mdp on mdp.parent = td.distribution_id and mdp.month = "%s"
    #     where 
    #         st.sales_person = "%s" 
    #         and td.fiscal_year = "%s"
    #         and MONTHNAME(si.posting_date) = "%s"
    #         and si.docstatus != 2
    #     group by sii.item_code, sii.item_group
    # """%(month, sales_person, fiscal_year, month)
    query = """
        SELECT 
            sii.item_code,
            td.item_group,
            COALESCE(SUM(sii.stock_qty), 0) AS qty,
            COALESCE(SUM(sii.amount), 0) AS amount,
            td.target_type,
            ROUND(td.target_qty * (mdp.percentage_allocation / 100)) AS target_volume,
            td.target_amount
        FROM `tabTarget Detail` AS td
        LEFT JOIN `tabMonthly Distribution Percentage` AS mdp 
            ON mdp.parent = td.distribution_id 
        AND mdp.month = "%s"
        LEFT JOIN `tabSales Invoice Item` AS sii 
            ON sii.item_group = td.item_group
        LEFT JOIN `tabSales Invoice` AS si 
            ON si.name = sii.parent
        AND MONTHNAME(si.posting_date) = "%s"
        AND si.docstatus != 2
        LEFT JOIN `tabSales Team` AS st 
            ON st.parent = si.name
        AND st.sales_person = "%s"
        WHERE td.fiscal_year = "%s"
        GROUP BY sii.item_code, td.item_group
    """ % (month, month, sales_person, fiscal_year)
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
            # "items": v,
            "items": [] if len(v) == 1 and v[0].get("item_code") is None else v,
            "total_qty": convert_to_uom(sum(item["qty"] for item in v), uom),
            "total_amount": shorten_amount(sum(item["amount"] for item in v), currency_symbol),
            "target_type": v[0]["target_type"],
            "total_target_volume": convert_to_uom(v[0]["target_volume"], uom),
            "total_target_amount": shorten_amount(v[0]["target_amount"], currency_symbol),
        }
        if v[0]["target_type"] != "Volume":
            item_group_targets[k].update({"achieved_percent": round((sum(item["amount"] for item in v) / v[0]["target_amount"])*100, 2) if v[0]["target_amount"] else 0, "uom": "KGS"})
        else:
            item_group_targets[k].update({"achieved_percent": round((sum(item["qty"] for item in v) / v[0]["target_volume"])*100, 2) if v[0]["target_volume"] else 0, })
        for item in v:
            item["amount"] = shorten_amount(item["amount"], currency_symbol)
            item["target_amount"] = shorten_amount(item["target_amount"], currency_symbol)
            item["qty"] = convert_to_uom(item["qty"], uom)
            item["target_volume"] = convert_to_uom(item["target_volume"], uom)
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
            left join `tabSales Team` as st on st.parent = si.name
            left join `tabSales Person` as sp on sp.name = st.sales_person
            left join `tabEmployee` as e on e.name = sp.employee
            left join `tabSales Invoice Item` as sii on sii.parent = si.name
            left join `tabTarget Detail` as td on td.item_group = sii.item_group
            left join `tabMonthly Distribution Percentage` as mdp on mdp.parent = td.distribution_id and mdp.month = "%s"
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
        self_board = []
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
            if user_image: overall["image"] = get_signed_token(user_image)
            overall.update({"name": employee_name})
            if user_id == frappe.session.user: 
                overall["session_user"] = True
            overall_persons.append(overall)
        overall_persons = sorted(
            overall_persons,
            key=lambda x: (x["total_percent"], x["name"]),
            reverse=True
        )
        overall_persons = [{"rank": rank, **person} for rank, person in enumerate(overall_persons, start=1)]
        top_three = overall_persons[:3]
        remaining = overall_persons[3:]
        self_board = next(filter(lambda x: x["session_user"], overall_persons), {})
        leader_board = [{
            "top_three": top_three,
            "leader_board": remaining,
            "self_board": self_board
        }]
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Leadboard fetched successfully"
        frappe.local.response['data'] = leader_board
    except Exception as err:
        get_exception(err)

def convert_to_uom(value, uom):
    return f"{value} {uom}"

def shorten_amount(amount, currency_symbol):
    if amount < 1000:
        return f"{currency_symbol}" + str(amount)
    if amount < 100000:
        return f"{currency_symbol}" + str(round(amount/1000, 1)) + "K"
    if amount < 10000000:
        return f"{currency_symbol}" + str(round(amount/100000, 1)) + "L"
    if amount < 1000000000:
        return f"{currency_symbol}" + str(round(amount/10000000, 1)) + "Cr"
    return f"{currency_symbol}" + str(round(amount/1000000000, 1)) + "B"
