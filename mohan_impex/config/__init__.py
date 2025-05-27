import frappe

def get_contact_list(party_type, party_name):
    contact_list = frappe.get_all("Dynamic Link", {"link_doctype": party_type, "link_name": party_name, "parenttype":"Contact Number"}, ["parent"], pluck="parent")
    return contact_list

def get_address_list(party_type, party_name):
    address_list = frappe.get_all("Dynamic Link", {"link_doctype": party_type, "link_name": party_name, "parenttype":"Address"}, ["parent"], pluck="parent")
    return address_list

@frappe.whitelist()
def get_contacts(verific_type=None, customer=None, unv_customer=None):
    contacts = []
    if verific_type == "Verified" and customer:
        contacts = get_contact_list("Customer", customer)
    elif verific_type == "Unverified" and unv_customer:
        contacts = frappe.get_all("Contact List", {"parent": unv_customer}, ["contact"], pluck="contact")
    return contacts

@frappe.whitelist()
def get_addresses(verific_type, customer=None, unv_customer=None):
    addresses = []
    if verific_type == "Verified" and customer:
        addresses = get_address_list("Customer", customer)
    elif verific_type == "Unverified" and unv_customer:
        addresses = frappe.get_all("Unverified Customer", {"name": unv_customer}, ["address"], pluck="address")
    return addresses