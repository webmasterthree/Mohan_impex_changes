# import frappe

# @frappe.whitelist()
# def get_journey_plan_with_trips():
#     data = []
#     plans = frappe.db.get_all(
#         "Journey Plan",
#         fields=["name", "visit_date", "nature_of_travel", "remarks"]
#     )

#     for plan in plans:
#         trips = frappe.db.get_all(
#             "Trips",
#             fields=[
#                 "primary_customer",
#                 "secondary_customer",
#                 "mode_of_travel",
#                 "travel_state_from",
#                 "travel_from_district",
#                 "travel_from_city",
#                 "travel_to_state",
#                 "travel_to_district",
#                 "travel_to_city"
#             ],
#             filters={"parent": plan.name, "parenttype": "Journey Plan"},
#             order_by="idx asc"
#         )

#         # 🔹 Convert CSV fields to list
#         for t in trips:
#             t["primary_customer"] = (
#                 [p.strip() for p in (t.get("primary_customer") or "").split(",") if p.strip()]
#                 if t.get("primary_customer") else []
#             )
#             t["secondary_customer"] = (
#                 [s.strip() for s in (t.get("secondary_customer") or "").split(",") if s.strip()]
#                 if t.get("secondary_customer") else []
#             )

#         plan["trips"] = trips
#         data.append(plan)

#     return data


import json
import frappe


# -------------------- GET: Prefill form --------------------
@frappe.whitelist(methods=["GET"])
def get_journey_plan_for_edit(name=None):
    """
    Get a single Journey Plan with trips in a form-friendly shape.

    Example:
      /api/method/mohan_impex.api.journey_plan.get_journey_plan_for_edit?name=JP-2025-10-00028
    """
    # Accept name from query args or direct argument
    name = name or frappe.form_dict.get("name")
    if not name:
        frappe.throw("Missing required parameter: name")

    doc = frappe.get_doc("Journey Plan", name)

    trips = frappe.db.get_all(
        "Trips",
        fields=[
            "name", "idx",
            "primary_customer", "secondary_customer",
            "mode_of_travel",
            "travel_state_from", "travel_from_district", "travel_from_city",
            "travel_to_state", "travel_to_district", "travel_to_city",
        ],
        filters={"parent": doc.name, "parenttype": "Journey Plan"},
        order_by="idx asc"
    )

    # Convert CSV to list
    def csv_to_list(v):
        if not v:
            return []
        return [p.strip() for p in str(v).split(",") if p.strip()]

    for t in trips:
        t["primary_customer"] = csv_to_list(t.get("primary_customer"))
        t["secondary_customer"] = csv_to_list(t.get("secondary_customer"))

    return {
        "name": doc.name,
        "visit_date": doc.get("visit_date"),
        "nature_of_travel": doc.get("nature_of_travel"),
        "remarks": doc.get("remarks"),
        "trips": trips,
    }


# -------------------- PUT: Edit form (partial) --------------------
import json
import frappe

@frappe.whitelist(methods=["PUT"])
def edit_journey_plan():
    """
    Update Journey Plan fields partially (only fields provided).
    Accepts ?name=JP-2025-10-00028 or { "name": "JP-2025-10-00028" } in body.
    """
    try:
        # Parse name from all possible sources
        name = None

        # 1️⃣ Try query param (?name=JP-2025-10-00028)
        if frappe.request and frappe.request.args:
            name = frappe.request.args.get("name")

        # 2️⃣ Try form_dict (for POST fallback)
        if not name and frappe.form_dict:
            name = frappe.form_dict.get("name")

        # 3️⃣ Try JSON body
        data = {}
        if frappe.request and frappe.request.data:
            try:
                data = json.loads(frappe.request.data)
                if not name:
                    name = data.get("name")
            except Exception:
                data = {}

        if not name:
            frappe.local.response["http_status_code"] = 400
            frappe.local.response["status"] = False
            frappe.local.response["message"] = "Missing Journey Plan name"
            return

        # Load the document
        doc = frappe.get_doc("Journey Plan", name)

        # Update parent fields
        for field in ["visit_date", "nature_of_travel", "remarks"]:
            if field in data:
                doc.set(field, data.get(field))

        # Save
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.local.response["status"] = True
        frappe.local.response["message"] = "Journey Plan updated successfully"
        frappe.local.response["data"] = {
            "name": doc.name,
            "visit_date": doc.visit_date,
            "nature_of_travel": doc.nature_of_travel,
            "remarks": doc.remarks
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "edit_journey_plan_error")
        frappe.local.response["http_status_code"] = 500
        frappe.local.response["status"] = False
        frappe.local.response["message"] = str(e)
