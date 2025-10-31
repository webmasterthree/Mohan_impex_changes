# import frappe
# from collections import defaultdict

# @frappe.whitelist()
# def get_mode_roles_map():
#     modes = frappe.get_all("Mode of Travel", pluck="name")
#     if not modes:
#         return {}

#     role_rows = frappe.get_all(
#         "Role Item",
#         fields=["parent as mode", "role", "idx"],
#         filters={
#             "parenttype": "Mode of Travel",
#             "parentfield": "roles",
#             "parent": ["in", modes],
#         },
#         order_by="parent asc, idx asc",
#     )

#     mode_to_roles = defaultdict(list)
#     for r in role_rows:
#         mode_to_roles[r["mode"]].append(r["role"])

#     return dict(mode_to_roles)

import frappe

@frappe.whitelist()
def get_modes_for_user(user: str | None = None):
    user = user or frappe.session.user
    roles = frappe.get_roles(user)

    if not roles:
        return []

    parents = frappe.get_all(
        "Role Item",
        filters={
            "parenttype": "Mode of Travel",
            "parentfield": "roles",
            "role": ["in", roles],
        },
        pluck="parent",
        distinct=True,
    )
    # keep a stable order
    if not parents:
        return []

    all_modes = set(parents)
    # Optional: ensure only existing Mode of Travel names are returned (and sorted)
    existing = frappe.get_all("Mode of Travel", filters={"name": ["in", list(all_modes)]}, pluck="name")
    return sorted(existing)
