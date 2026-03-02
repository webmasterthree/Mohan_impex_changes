import frappe
from frappe.utils import money_in_words

@frappe.whitelist()
def get_money_in_words(amount):
    return money_in_words(amount)



@frappe.whitelist()
def weight_in_words(amount):
    text = money_in_words(amount) or ""
    text = text.replace("INR ", "").replace("Rs. ", "")
    if " and " in text:
        text = text.split(" and ")[0]
    text = text.replace(" only.", "").replace(" only", "")
    return text.strip()