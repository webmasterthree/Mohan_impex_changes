import frappe
from frappe.utils import money_in_words

@frappe.whitelist()
def get_money_in_words(amount):
    return money_in_words(amount)
