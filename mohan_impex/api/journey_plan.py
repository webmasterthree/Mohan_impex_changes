import frappe
from mohan_impex.mohan_impex.utils import get_session_employee_area, get_session_employee, get_session_emp_role
import math
from mohan_impex.mohan_impex.comment import get_comments
from mohan_impex.api import get_role_filter, get_self_filter_status, get_exception, get_workflow_statuses, has_create_perm
from mohan_impex.api.location_id import get_city_id, get_district_id, get_state_id



@frappe.whitelist()
def journey_plan_list():
    try:
        tab = frappe.form_dict.get("tab")
        limit = frappe.form_dict.get("limit")
        is_self = frappe.form_dict.get("is_self")
        other_employee = frappe.form_dict.get("employee")
        current_page = frappe.form_dict.get("current_page")

        # Basic validations
        if not tab:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please give the list tab"
            return

        if not limit or not current_page:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Either limit or current page is missing"
            return

        # Pagination
        current_page = int(current_page)
        limit = int(limit)
        offset = limit * (current_page - 1)
        pagination = "limit %s offset %s" % (limit, offset)

        # Tab filter (workflow)
        if tab == "Pending":
            tab_filter = 'jp.workflow_state != "Approved"'
        else:
            tab_filter = 'jp.workflow_state = "%s"' % (tab)

        # Role visibility filter
        emp = frappe.get_value(
            "Employee",
            {"user_id": frappe.session.user},
            ["name", "area", "role_profile"],
            as_dict=True,
        )
        role_filter = get_role_filter(emp, is_self, other_employee)
        is_self_filter = get_self_filter_status()
        order_by = " order by jp.creation desc "

        # Base query
        query = """
            SELECT 
                jp.name, 
                jp.created_date,
                jp.visit_date,
                IF(jp.workflow_state='Approved', jp.approved_date, 
                   IF(jp.workflow_state='Rejected', jp.rejected_date, jp.created_date)) AS status_date, 
                jp.workflow_state AS status, 
                jp.created_by_emp, 
                jp.created_by_name, 
                COUNT(*) OVER() AS total_count
            FROM `tabJourney Plan` jp
            LEFT JOIN `tabTrips` t ON t.parent = jp.name
            WHERE {tab_filter} AND {role_filter}
        """.format(tab_filter=tab_filter, role_filter=role_filter)

        # Frontend → DB field map
        filter_checks = {
            # Only visit_date is used for the date filter now
            "date": "jp.visit_date",
            "status": "jp.workflow_state",
            "nature_of_travel": "jp.nature_of_travel",
            "mode_of_travel": "t.mode_of_travel",  # child table field
        }

        # Free text search on docname
        if frappe.form_dict.get("search_text"):
            search_text = frappe.form_dict.get("search_text")
            query += ' AND (jp.name LIKE "%{0}%")'.format(search_text)

        # Structured filters (date → jp.visit_date only)
        and_filters = []
        for key, value in filter_checks.items():
            if frappe.form_dict.get(key):
                if key == "date":
                    date_val = frappe.form_dict[key]
                    and_filters.append(' {0} = "{1}" '.format(value, date_val))
                else:
                    and_filters.append(' {0} = "{1}" '.format(value, frappe.form_dict[key]))

        if and_filters:
            query += " AND (" + " AND ".join(and_filters) + ")"

        # Finalize query
        query += order_by
        query += pagination

        # Execute
        journey_info = frappe.db.sql(query, as_dict=True)

        # Add form URL per record
        base_url = frappe.utils.get_url()
        for journey in journey_info:
            journey["form_url"] = (
                f"{base_url}/api/method/mohan_impex.api.journey_plan.journey_form?name={journey['name']}"
            )

        # Pagination metadata
        total_count = journey_info[0]["total_count"] if journey_info else 0
        page_count = math.ceil(total_count / int(limit)) if limit else 0

        response = [
            {
                "records": journey_info,
                "total_count": total_count,
                "page_count": page_count,
                "current_page": current_page,
                "has_toggle_filter": is_self_filter,
                "create": has_create_perm("Journey Plan"),
            }
        ]

        # API response
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Journey Plan list has been successfully fetched"
        frappe.local.response['data'] = response

    except Exception as err:
        get_exception(err)



@frappe.whitelist(methods=["GET"])
def journey_plan_form():
	journey_name = frappe.form_dict.get("name")
	try:
		if not journey_name:
			frappe.local.response["http_status_code"] = 400
			frappe.local.response["status"] = False
			frappe.local.response["message"] = "Please provide Journey Plan ID in 'name'."
			return

		if not frappe.db.exists("Journey Plan", journey_name):
			frappe.local.response["http_status_code"] = 404
			frappe.local.response["status"] = False
			frappe.local.response["message"] = "Please give valid Journey Plan ID"
			return

		journey_doc = frappe.get_doc("Journey Plan", journey_name)
		journey_doc = journey_doc.as_dict()

		journey_doc["doctype"] = journey_doc.get("doctype") or "Journey Plan"
		journey_doc["workflow_state"] = journey_doc.get("workflow_state")

		fields = [
			"name",
			"idx",
			"primary_customer",
			"secondary_customer",
			"mode_of_travel",
			"travel_state_from",
			"travel_from_district",
			"travel_from_city",
			"travel_to_state",
			"travel_to_district",
			"travel_to_city",
		]

		trips = frappe.db.get_all(
			"Trips",
			fields=fields,
			filters={"parent": journey_doc["name"], "parenttype": "Journey Plan"},
			order_by="idx asc",
		)

		def csv_to_list(value):
			if not value:
				return []
			return [v.strip() for v in str(value).split(",") if v.strip()]

		for trip in trips:
			# CSV → list
			trip["primary_customer"] = csv_to_list(trip.get("primary_customer"))
			trip["secondary_customer"] = csv_to_list(trip.get("secondary_customer"))

			# ---- Preserve value, insert *_id first, then value ----

			# FROM State
			travel_state_from = trip.pop("travel_state_from", None)
			trip["travel_state_from_id"] = get_state_id(travel_state_from) if travel_state_from else ""
			trip["travel_state_from"] = travel_state_from

			# FROM District
			travel_from_district = trip.pop("travel_from_district", None)
			trip["travel_from_district_id"] = (
				get_district_id(travel_from_district) if travel_from_district else ""
			)
			trip["travel_from_district"] = travel_from_district

			# FROM City
			travel_from_city = trip.pop("travel_from_city", None)
			trip["travel_from_city_id"] = get_city_id(travel_from_city) if travel_from_city else ""
			trip["travel_from_city"] = travel_from_city

			# TO State
			travel_to_state = trip.pop("travel_to_state", None)
			trip["travel_to_state_id"] = get_state_id(travel_to_state) if travel_to_state else ""
			trip["travel_to_state"] = travel_to_state

			# TO District
			travel_to_district = trip.pop("travel_to_district", None)
			trip["travel_to_district_id"] = (
				get_district_id(travel_to_district) if travel_to_district else ""
			)
			trip["travel_to_district"] = travel_to_district

			# TO City
			travel_to_city = trip.pop("travel_to_city", None)
			trip["travel_to_city_id"] = get_city_id(travel_to_city) if travel_to_city else ""
			trip["travel_to_city"] = travel_to_city

		journey_doc["trips"] = trips

		activities = get_comments("Journey Plan", journey_doc["name"])
		journey_doc["activities"] = activities or []

		is_self_filter = get_self_filter_status()
		journey_doc["status_fields"] = (
			get_workflow_statuses("Journey Plan", journey_name, get_session_emp_role()) or []
		)

		journey_doc["has_toggle_filter"] = 1 if is_self_filter else 0

		journey_doc["created_person_mobile_no"] = frappe.get_value(
			"Employee",
			journey_doc.get("created_by_emp"),
			"custom_personal_mobile_number",
		)

		frappe.local.response["status"] = True
		frappe.local.response["message"] = "Journey Plan has been successfully fetched"
		frappe.local.response["data"] = [journey_doc]

	except Exception as err:
		get_exception(err)




    
@frappe.whitelist()
def create_journey_plan():
    journey_plan_data = frappe.form_dict
    journey_plan_data.pop("cmd")
    journey_plan_data.update({
        "doctype" : "Journey Plan",
        "created_by_emp": get_session_employee(),
        "area": get_session_employee_area()
    })
    try:
        journey_plan_doc = frappe.get_doc(journey_plan_data)
        journey_plan_doc.save()
        response = {
            "journey_plan": journey_plan_doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Journey Plan has been successfully created"
        frappe.local.response['data'] = [response]
    except Exception as err:
        get_exception(err)


@frappe.whitelist(methods=["POST"])
def update_journey_plan():
    try:
        payload = frappe.request.get_json(silent=True) or {}
        journey_name = payload.get("name") or frappe.form_dict.get("name")

        if not journey_name:
            frappe.local.response["http_status_code"] = 400
            frappe.local.response["status"] = False
            frappe.local.response["message"] = "Please provide Journey Plan ID in 'name'."
            return

        if not frappe.db.exists("Journey Plan", journey_name):
            frappe.local.response["http_status_code"] = 404
            frappe.local.response["status"] = False
            frappe.local.response["message"] = "Please give valid Journey Plan ID"
            return

        doc = frappe.get_doc("Journey Plan", journey_name)

        header_fields = [
            "visit_date",
            "nature_of_travel",
            "remarks",
            "area",
            "workflow_state",
            "approved_date",
            "rejected_date",
        ]
        for field in header_fields:
            if field in payload:
                doc.set(field, payload[field])

        doc.workflow_state = "Pending"
        doc.status = "Pending"

        if "trips" in payload and isinstance(payload["trips"], list):
            doc.set("trips", [])
            for row in payload["trips"]:
                doc.append("trips", {
                    "primary_customer": row.get("primary_customer"),
                    "secondary_customer": row.get("secondary_customer"),
                    "mode_of_travel": row.get("mode_of_travel"),
                    "travel_state_from": row.get("travel_state_from"),
                    "travel_from_district": row.get("travel_from_district"),
                    "travel_from_city": row.get("travel_from_city"),
                    "travel_to_state": row.get("travel_to_state"),
                    "travel_to_district": row.get("travel_to_district"),
                    "travel_to_city": row.get("travel_to_city"),
                })

        doc.save(ignore_permissions=True)
        frappe.db.commit()

        journey_doc = doc.as_dict()
        activities = get_comments("Journey Plan", journey_doc["name"])
        journey_doc["activities"] = activities

        is_self_filter = get_self_filter_status()
        journey_doc["status_fields"] = get_workflow_statuses(
            "Journey Plan", journey_name, get_session_emp_role()
        )
        journey_doc["has_toggle_filter"] = is_self_filter

        journey_doc["created_person_mobile_no"] = frappe.get_value(
            "Employee",
            journey_doc.get("created_by_emp"),
            "custom_personal_mobile_number",
        )

        frappe.local.response["status"] = True
        frappe.local.response["message"] = "Journey Plan has been successfully updated"
        frappe.local.response["data"] = [journey_doc]

    except Exception as err:
        get_exception(err)
