# import frappe
# import json

# def get_supplier_portal_users():
#     suppliers = frappe.db.get_all("Supplier", fields=["name"])  # Fetch all supplier names
    
#     supplier_data = []

#     for supplier in suppliers:
#         portal_users = frappe.db.get_all(
#             "Portal User",
#             filters={"parent": supplier["name"], "parenttype": "Supplier"},
#             fields=["user"]  # Only fetch the 'user' field
#         )

#         if portal_users:
#             supplier_data.append({
#                 "supplier": supplier["name"],
#                 "portal_users": [user["user"] for user in portal_users]  # Extracting only user emails
#             })

#     return json.dumps(supplier_data, indent=4)  # Convert list to JSON format with indentation

# # Call function and print output
# supplier_portal_users_json = get_supplier_portal_users()
# print(supplier_portal_users_json)


import frappe
import json

@frappe.whitelist()
def get_supplier_portal_users(user_email=None):
    if not user_email:
        user_email = frappe.session.user  # Get the logged-in user

    portal_user = frappe.db.get_all(
        "Portal User",
        filters={"user": user_email, "parenttype": "Supplier"},
        fields=["parent"]  # Fetch only the Supplier name
    )

    if portal_user:
        return [{"supplier": portal_user[0]["parent"]}]  # Return supplier name

    return []
