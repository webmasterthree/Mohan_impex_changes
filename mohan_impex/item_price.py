import frappe

@frappe.whitelist()
def get_item_category_price(item, item_category, price_list="Standard Selling"):
    query = '''
        select price_list_rate 
        from `tabItem Price` as ip
        where item_code = "{item}" and item_category = "{item_category}" and price_list = "{price_list}" order by creation desc limit 1
    '''.format(item=item, item_category=item_category, price_list=price_list)
    rate = frappe.db.sql(query, as_dict=1)
    item_rate = 0
    if rate:
        item_rate = rate[0]["price_list_rate"]
    return item_rate