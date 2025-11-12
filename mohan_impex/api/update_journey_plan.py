import json
import frappe

def _list_to_csv(val):
    if isinstance(val, list):
        cleaned = [str(x).strip() for x in val if str(x).strip()]
        return ", ".join(cleaned)
    # allow single string passthrough
    return (val or "").strip() if isinstance(val, str) else val

def _csv_to_list(val):
    if not val:
        return []
    return [p.strip() for p in str(val).split(",") if p.strip()]

@frappe.whitelist(methods=["PUT"])
def edit_journey_plan():
    """
    Partial update for Journey Plan + Trips.
    Accepts ?name=JP-2025-10-00028 and/or {"name": "..."} in body.
    Trips accepts arrays for customers and stores as CSV.
    After update -> workflow_state=status='Pending' (if fields exist).
    """
    try:
        # ---- resolve name ----
        name = None
        if frappe.request and frappe.request.args:
            name = frappe.request.args.get("name")
        if not name and frappe.form_dict:
            name = frappe.form_dict.get("name")

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

        # ---- load doc ----
        doc = frappe.get_doc("Journey Plan", name)

        # ---- parent partial patch ----
        for field in ["visit_date", "nature_of_travel", "remarks"]:
            if field in data:
                doc.set(field, data.get(field))

        # ---- trips patch ----
        trips_payload = data.get("trips", [])
        if isinstance(trips_payload, list) and trips_payload:
            # index existing by child name
            existing_by_name = {row.name: row for row in (doc.trips or [])}

            for t in trips_payload:
                if not isinstance(t, dict):
                    continue

                # find or create row
                row = None
                child_name = (t.get("name") or "").strip()
                if child_name and child_name in existing_by_name:
                    row = existing_by_name[child_name]
                else:
                    row = doc.append("trips", {})

                # explicit handling for customer arrays -> CSV
                if "primary_customer" in t:
                    row.set("primary_customer", _list_to_csv(t.get("primary_customer")))
                    row.flags.dirty = True  # ensure frappe persists the change

                if "secondary_customer" in t:
                    row.set("secondary_customer", _list_to_csv(t.get("secondary_customer")))
                    row.flags.dirty = True

                # set remaining fields if they exist on the child doctype
                for k, v in t.items():
                    if k in {"name", "parent", "parenttype", "parentfield", "idx", "doctype",
                             "primary_customer", "secondary_customer"}:
                        continue
                    if k in row.as_dict():
                        row.set(k, v)
                        row.flags.dirty = True

        # ---- force Pending ----
        if doc.meta.get_field("workflow_state"):
            doc.workflow_state = "Pending"
        if doc.meta.get_field("status"):
            doc.status = "Pending"

        # ---- save ----
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        # ---- build fresh response (CSV -> arrays) ----
        refreshed = frappe.get_doc("Journey Plan", name)
        trips = frappe.db.get_all(
            "Trips",
            fields=[
                "name", "idx",
                "primary_customer", "secondary_customer",
                "mode_of_travel",
                "travel_state_from", "travel_from_district", "travel_from_city",
                "travel_to_state", "travel_to_district", "travel_to_city",
            ],
            filters={"parent": refreshed.name, "parenttype": "Journey Plan"},
            order_by="idx asc"
        )
        for t in trips:
            t["primary_customer"] = _csv_to_list(t.get("primary_customer"))
            t["secondary_customer"] = _csv_to_list(t.get("secondary_customer"))

        frappe.local.response["status"] = True
        frappe.local.response["message"] = "Journey Plan updated successfully"
        frappe.local.response["data"] = {
            "name": refreshed.name,
            "visit_date": refreshed.get("visit_date"),
            "nature_of_travel": refreshed.get("nature_of_travel"),
            "remarks": refreshed.get("remarks"),
            "workflow_state": getattr(refreshed, "workflow_state", None),
            "status": getattr(refreshed, "status", None),
            "trips": trips
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "edit_journey_plan_error")
        frappe.local.response["http_status_code"] = 500
        frappe.local.response["status"] = False
        frappe.local.response["message"] = str(e)
