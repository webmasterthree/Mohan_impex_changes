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
