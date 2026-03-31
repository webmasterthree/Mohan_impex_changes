import frappe
import jwt
import mimetypes
from frappe import _  # Translation support
from frappe.utils import now_datetime, get_datetime, get_url
from frappe.utils.file_manager import get_file_path
from werkzeug.wrappers import Response
import requests
from mohan_impex.mohan_impex.utils import get_session_employee
from frappe.utils.nestedset import get_descendants_of
from bs4 import BeautifulSoup
import json
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from frappe.model.workflow import get_transitions

@frappe.whitelist()
def dashboard():
    score_dash_schema = {
        "Trial Plan": "Trial",
        "Sales Order": "Orders",
        "Customer Visit Management": "Visits"
    }
    score_dash = []
    for doctype, label in score_dash_schema.items():
        if frappe.has_permission(doctype):
            score_dash.append(get_score_dash_info(doctype, label))
    dashboard = []
    dashboard_schema =  frappe.db.get_all("Dashboard Info", ["*"])
    for dash_dict in dashboard_schema:
        if not dash_dict["is_group"] and not dash_dict["parent_dashboard_info"]:
            if frappe.has_permission(dash_dict["doc_name"]):
                dashboard.append({
                    "name": dash_dict["title"],
                    "url":get_dash_info(dash_dict["list_api_endpoint"], type="endpoint"),
                    "image_url": get_dash_info(dash_dict["image"], type="image"),
                    "order": dash_dict["order"]
                })
        elif dash_dict["is_group"]:
            child = list(filter(lambda x: x["parent_dashboard_info"] == dash_dict["name"] and frappe.has_permission(x["doc_name"]), dashboard_schema))
            if child:
                child_list = []
                for child_dict in child:
                    child_list.append({
                        "name": child_dict["title"],
                        "url":get_dash_info(child_dict["list_api_endpoint"], type="endpoint"),
                        "image_url": get_dash_info(child_dict["image"], type="image"),
                        "order": child_dict["order"]
                })
                child_list = sorted(child_list, key=lambda x: x.get("order", 0))
                dashboard.append({
                    "name": dash_dict["title"],
                    "url":get_dash_info(dash_dict["list_api_endpoint"], type="endpoint"),
                    "image_url": get_dash_info(dash_dict["image"], type="image"),
                    "order": dash_dict["order"],
                    "child": child_list 
                })
    dashboard = sorted(dashboard, key=lambda x: x.get("order", 0))
    last_log = get_last_checkin_info()
    banner_info = get_banners()
    response = {
        "score_dashboard": score_dash,
        "dashboard":  dashboard,
        "last_log": last_log,
        "banner_info": banner_info
    }
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Dashboard Info fetched successfully"
    frappe.local.response['data'] = [response]


def get_score_dash_info(doctype, label):
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
    if doctype == "Customer Visit Management":
        dash_info = frappe.get_list(doctype, {"created_by_emp": emp.get("name"), "docstatus": 1}, [f"'{label}' as name, count(name) as count"])[0]
    elif doctype == "Sales Order":
        dash_info = frappe.get_list(doctype, {"created_by_emp": emp.get("name"), "docstatus": 1}, [f"'{label}' as name, count(name) as count"])[0]
    elif doctype == "Trial Plan":
        dash_info = frappe.get_list(doctype, {"created_by_emp": emp.get("name"), "docstatus": 1}, [f"'{label}' as name, count(name) as count"])[0]
    return dash_info

def get_dash_info(url, type):
    site_url = frappe.utils.get_url()  # Gets the site URL
    if type == "endpoint":
        url = f"{site_url}/app/method/{url}"
    elif type == "image" and url:
        url = get_signed_token(url)
    return url

def get_banners():
    banner_info = frappe.get_all("Banners", ["banner_name", "banner_image"])
    for banner in banner_info:
        banner["banner_image"] = get_signed_token(banner["banner_image"])
    return banner_info

def get_last_checkin_info():
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, "name")
    try:
        last_checkin = frappe.get_last_doc("Employee Checkin", filters={"employee": emp})
        last_log = [{
            "last_log_type": last_checkin.log_type,
            "last_log_time": last_checkin.time
        }]
        return last_log
    except frappe.DoesNotExistError as err:
        return []

@frappe.whitelist(methods=["POST"])
def checkin(employee, datetime, log_type, latitude, longitude):
    try:
        doc = frappe.get_doc({
            "doctype":'Employee Checkin', 
            "employee" : employee,
            "time" : datetime, #2025-02-04 14:19:01
            "log_type" : log_type,
            "latitude": latitude,
            "longitude": longitude
        })
        doc.save()
        response = {
            "emp_checkin": doc.name
        }
        frappe.local.response['status'] = True
        frappe.local.response['message'] = f"Successfully Checked {log_type.lower()}"
        frappe.local.response['data'] = [response]
    except Exception as err:
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"{err}"
        frappe.local.response['data'] = []

def create_contact(contactno, doctype=None, link_name=None):
    if not frappe.db.exists("Contact", contactno):
        doc=frappe.get_doc({
            "doctype":"Contact",
            "first_name": contactno,
        })
        doc.save(ignore_permissions=True)
    if doctype and link_name:
        contact_link = frappe.get_doc({
            "doctype": "Dynamic Link",
            "parenttype": "Contact",
            "parent": contactno,
            "parentfield": "links",
            "link_doctype": doctype,
            "link_name": link_name
        })
        contact_link.save(ignore_permissions=True)

def create_contact_number(contactno, doctype=None, link_name=None):
    import re
    if not re.match(r'^\d{10}$', contactno):
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"Contact Number {contactno} must be a 10 digit mobile number"
        return
    if frappe.db.exists("Contact Number", contactno):
        contact_doc = frappe.get_doc("Contact Number", contactno)
    else:
        contact_doc = frappe.new_doc("Contact Number")
        contact_dict = {
            "contact_number": contactno
        }
        contact_doc.update(contact_dict)
    if doctype and link_name:
        link_exists = frappe.db.exists("Dynamic Link", {"link_doctype": doctype, "link_name": link_name, "parenttype": "Contact Number"})
        if not link_exists:
            contact_doc.append("links", {
                "link_doctype": doctype,
                "link_name": link_name
            })
    contact_doc.save(ignore_permissions=True)
    return contact_doc

@frappe.whitelist()
def upload_attachments():
    if not frappe.request.files:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Image Files Not Found"
        return
    response = []
    for key in frappe.request.files:
        file = frappe.request.files[key]
        filename = file.filename
        file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": filename,
                "content": file.read(),
            })
        file_doc.insert(ignore_permissions=True)  # Insert the file document
        frappe.db.commit()
        response.append({
            "name": file_doc.name,
            "file_name": file_doc.file_name,
            "file_url": file_doc.file_url,
            "url": frappe.utils.get_url() + file_doc.file_url
        })
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "The given douments has been successfully uploaded in the system"
    frappe.local.response['data'] = response

@frappe.whitelist()
def get_channel_partner(search_text=""):
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
    role_filter = get_territory_role_filter(emp)
    # if emp:
    #     role_filter = f"""and created_by_emp = "{emp.get('name')}" """
    query = f"""
        SELECT cu.name, customer_name
        FROM `tabCustomer` AS cu
        LEFT JOIN `tabDynamic Link` as dl on dl.link_name = cu.name
        LEFT JOIN `tabContact Number` AS ct on ct.name = dl.parent
        WHERE is_dl=1 and {role_filter}
    """.format(role_filter=role_filter)
    if search_text:
        search_cond = """ AND (cu.customer_name LIKE "%{search_text}%" or ct.name LIKE "%{search_text}%") """.format(search_text=search_text)
        query += search_cond
    query += "GROUP BY cu.name"
    companies = frappe.db.sql(query, as_dict=1)
    return companies

@frappe.whitelist()
def get_shops(search_text=""):
    query = """
        SELECT name, shop_name
        FROM `tabShop` AS co
    """
    params = []
    if search_text:
        search_cond = """where name LIKE %s or contact LIKE %s"""
        con = "%{0}%".format(search_text)
        params.extend([con, con])
        query += search_cond
    shops = frappe.db.sql_list(query, params)
    return shops

@frappe.whitelist()
def get_item_templates():
    query = """
        select item_code, item_name, item_category
        from `tabItem`
        where has_variants = 1
    """
    if frappe.form_dict.get("search_text"):
        query += """ AND (item_name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
    item_templates = frappe.db.sql(query, as_dict=True)
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Items fetched successfully"
    frappe.local.response['data'] = item_templates

@frappe.whitelist()
def get_item_variants():
    query = """
        select i.item_code, i.item_name, i.item_category, cd.competitor, IF(i.sales_uom IS NOT NULL AND i.sales_uom != '', i.sales_uom, stock_uom) AS uom
        from `tabItem` as i
        left join `tabCompetitor Detail` as cd on cd.parent = i.name
        where has_variants = 0
    """
    # query = """
    #     SELECT i.item_code, i.item_name, i.item_category, c.name AS competitor, IF(i.sales_uom IS NOT NULL AND i.sales_uom != '', i.sales_uom, stock_uom) AS uom
    #     FROM `tabItem` AS i
    #     LEFT JOIN `tabCompetitor Item` AS ci ON i.name = ci.item_code
    #     LEFT JOIN `tabCompetitor` AS c ON c.name = ci.parent
    #     WHERE i.has_variants = 0
    # """
    if frappe.form_dict.get("item_template"):
        query += """ AND variant_of="{0}" """.format(frappe.form_dict.get("item_template"))
    if frappe.form_dict.get("item_category"):
        query += """ AND item_category="{0}" """.format(frappe.form_dict.get("item_category"))
    if frappe.form_dict.get("search_text"):
        query += """ AND (item_name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
    item_variants = frappe.db.sql(query, as_dict=True)
    consol_item_variants = competitor_consolidate(item_variants)
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Items fetched successfully"
    frappe.local.response['data'] = consol_item_variants

def competitor_consolidate(item_list):
    result = {}
    for item in item_list:
        key = (item["item_code"], item["item_name"], item["item_category"])
        if key not in result:
            result[key] = {
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "item_category": item["item_category"],
                "uom": item["uom"],
                "competitors": []
            }
        if item.get("competitor"):
            result[key]["competitors"].append(item["competitor"])
    consol_items = list(result.values())
    return consol_items

@frappe.whitelist()
def get_competitor_items():
    if not frappe.form_dict.get("competitor"):
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Please give the competitor value for filter"
        return
    query = """
        select distinct item_name
        from `tabCompetitor Item` as ci
        where parent is not null
    """
    if frappe.form_dict.get("competitor"):
        query += """ AND ci.parent="{0}" """.format(frappe.form_dict.get("competitor"))
    competitors = frappe.db.sql(query, as_dict=True)
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Competitor Items fetched successfully"
    frappe.local.response['data'] = competitors

@frappe.whitelist()
def get_items():
    query = """
        select i.item_code, i.item_name, i.item_category, IF(i.sales_uom IS NOT NULL AND i.sales_uom != '', i.sales_uom, stock_uom) AS uom
        from `tabItem` as i
        join `tabBase Components` as bc on bc.item_code = i.item_code
    """
    if frappe.form_dict.get("product"):
        query += """ and bc.parent = "{0}" """.format(frappe.form_dict.get("product"))
    if frappe.form_dict.get("item_category"):
        query += """ and i.item_category = "{0}" """.format(frappe.form_dict.get("item_category"))
    items = frappe.db.sql(query, as_dict=True)
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Items fetched successfully"
    frappe.local.response['data'] = items

@frappe.whitelist()
def material_list():
    try:
        query = """
            select item_code, item_name
            from `tabItem`
            where item_group="Marketing Collateral Material"
        """
        if frappe.form_dict.get("search_text"):
            or_filters = """where (item_code LIKE "%{search_text}%" or item_name LIKE "%{search_text}%") """.format(search_text=frappe.form_dict.get("search_text"))
            query += or_filters
        material_list = frappe.db.sql(query, as_dict=True)
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Material list fetched successfully"
        frappe.local.response['data'] = material_list
    except Exception as err:
        get_exception(err)


@frappe.whitelist()
def get_customer_list(search_text=""):
    emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
    area_role_filter = get_role_filter(emp)
    territory_role_filter = get_territory_role_filter(emp)
    customer_list = []
    filters = {}
    if search_text:
        filters.update({"search_text": search_text})
    if frappe.form_dict.get("channel_partner"):
        filters.update({"channel_partner": frappe.form_dict.get("channel_partner")})
    if frappe.form_dict.get("customer_level"):
        filters.update({"customer_level": frappe.form_dict.get("customer_level")})
    if frappe.form_dict.get("show_area_records"):
        filters.update({"show_area_records": frappe.form_dict.get("show_area_records")})
    if frappe.form_dict.get("verification_type"):
        if frappe.form_dict.get("verification_type") == "Verified":
            if frappe.form_dict.get("kyc_status"):
                filters.update({"kyc_status": frappe.form_dict.get("kyc_status")})
            customer_list.extend(get_customer_info(**filters, role_filter=territory_role_filter))
        elif frappe.form_dict.get("verification_type") == "Unverified":
            customer_list.extend(unv_customer_list(**filters, role_filter=area_role_filter))
    else:
        customer_list.extend(get_customer_info(**filters, role_filter=territory_role_filter))
        customer_list.extend(unv_customer_list(**filters, role_filter=area_role_filter))
    return customer_list

@frappe.whitelist()
def get_customer_info(role_filter=None, customer_level="", channel_partner="", kyc_status="", search_text=""):
    if not role_filter:
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_territory_role_filter(emp)
    query = """
        SELECT cu.name as name, cu.customer_name, cu.custom_shop as shop, cu.custom_shop_name as shop_name, ct.name as contact, cu.customer_level, cu.custom_channel_partner as channel_partner, cu.cp_name, cu.kyc_status
        FROM `tabCustomer` AS cu
        LEFT JOIN `tabDynamic Link` as dl on dl.link_name = cu.name
        LEFT JOIN `tabContact Number` AS ct on ct.name = dl.parent
        WHERE {role_filter} and cu.is_dl = 0
    """.format(role_filter=role_filter)
    if search_text:
        # or cu.custom_shop LIKE "%{search_text}%"
        search_cond = """ AND (cu.customer_name LIKE "%{search_text}%" or ct.name LIKE "%{search_text}%") """.format(search_text=search_text)
        query += search_cond
    if customer_level:
        query += """ AND cu.customer_level = "{0}" """.format(customer_level)
    if channel_partner:
        query += """ AND cu.custom_channel_partner = "{0}" """.format(channel_partner)
    if kyc_status:
        query += """ AND cu.kyc_status = "{0}" """.format(kyc_status)
    customers = frappe.db.sql(query, as_dict=True)
    result={}
    for entry in customers:
        key = entry["name"]
        if key not in result:
            result[key] = {
                "name": entry["name"],
                "customer_name": entry["customer_name"],
                "verific_type": "Verified",
                "customer_level": entry["customer_level"],
                "shop": entry["shop"],
                "shop_name": entry["shop_name"],
                "channel_partner": entry["channel_partner"],
                "cp_name": entry["cp_name"],
                "kyc_status": entry["kyc_status"],
                "contact": []
            }
        if entry["contact"]:
            result[key]["contact"].append(entry["contact"])
    customer_info = list(result.values())
    return customer_info

@frappe.whitelist()
def unv_customer_list(role_filter=None, customer_level="", channel_partner="", kyc_status="", search_text=""):
    try:
        if not role_filter:
            customer_level = "Primary"
        emp = frappe.get_value("Employee", {"user_id": frappe.session.user}, ["name", "area"], as_dict=True)
        role_filter = get_role_filter(emp)
        query = """
            select unv.name, customer_name, customer_level, shop, shop_name, contact, channel_partner, cp_name, kyc_status
            from `tabUnverified Customer` as unv
            LEFT JOIN `tabContact List` as cl on cl.parent = unv.name
            WHERE kyc_status = "Pending" and {role_filter}
        """.format(role_filter=role_filter)
        if frappe.form_dict.get("search_text"):
            # or unv.shop_name LIKE "%{search_text}%"
            or_filters = """ AND (unv.customer_name LIKE "%{search_text}%" or cl.contact LIKE "%{search_text}%") """.format(search_text=search_text)
            query += or_filters
        if customer_level:
            query += """ AND unv.customer_level = "{0}" """.format(customer_level)
        if channel_partner:
            query += """ AND unv.channel_partner = "{0}" """.format(channel_partner)
        unv_customer_list = frappe.db.sql(query, as_dict=True)
        result={}
        for entry in unv_customer_list:
            key = entry["name"]
            if key not in result:
                result[key] = {
                    "name": entry["name"],
                    "customer_name": entry["customer_name"],
                    "verific_type": "Unverified",
                    "customer_level": entry["customer_level"],
                    "shop": entry["shop"],
                    "shop_name": entry["shop_name"],
                    "channel_partner": entry["channel_partner"],
                    "kyc_status": entry["kyc_status"],
                    "contact": []
                }
            if entry["contact"]:
                result[key]["contact"].append(entry["contact"])
        unv_customer_list = list(result.values())
        if role_filter:
            return unv_customer_list
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Unverified Customer list fetched successfully"
        frappe.local.response['data'] = unv_customer_list
    except Exception as err:
        get_exception(err)

SECRET_KEY = frappe.local.conf.get("jwt_secret")
def get_signed_token(file_path, access_token=""):
    import jwt
    from frappe.utils import get_url, now_datetime, add_to_date
    if not file_path:
        return file_path
    if not access_token:
        auth_header = frappe.get_request_header("Authorization")
        access_token = auth_header.split(" ")[1]
    payload = {
        "access_token": access_token,
        "file_path": file_path,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    secure_url = f"{get_url()}/api/method/mohan_impex.api.protected_file?token={token}"
    return secure_url

@frappe.whitelist(allow_guest=True)
def protected_file(token):
    """Serve the file if access token is valid and file is in the allowed list."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        allowed_files = payload.get("file_path", "")
        access_token = payload.get("access_token", "")
        token_data = frappe.db.get_value("OAuth Bearer Token", {"access_token": access_token}, ["user", "expires_in", "expiration_time"], as_dict=True)
        
        if not token_data:
            frappe.throw("Invalid access token", frappe.AuthenticationError)

        # Check if the token is expired
        if token_data:
            if now_datetime() > get_datetime(token_data["expiration_time"]):
                frappe.throw("Access token has expired", frappe.AuthenticationError)
        if not allowed_files:
            return "Unauthorized Access", 403
        # Get the actual file path
        full_path = get_file_path(payload["file_path"])

        mime_type, _ = mimetypes.guess_type(full_path)

        # Read file data
        with open(full_path, "rb") as f:
            file_data = f.read()

        response = Response(file_data, content_type=mime_type or "application/octet-stream")
        # response.headers["Content-Disposition"] = f"""attachment; filename="{payload['file_path']}" """
        return response

    except jwt.ExpiredSignatureError:
        return "Token Expired", 403
    except Exception as e:
        frappe.log_error(f"File Access Error: {str(e)}")
        return "Invalid Token", 400

@frappe.whitelist()
def is_within_range(origin, destination):
    try:
        api_key = frappe.get_single("Google Settings").api_key
        if not api_key:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "NO API_KEY found in Google Settings"
            return
        origin_list = [x.strip() for x in origin.split(",") if x]
        if not (len(origin_list) == 2 and all([isinstance(float(x), float) for x in origin_list])):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Origin is not a valid float or not separated by comma"
            return
        
        destination_list = [x.strip() for x in destination.split(",")]
        if not (len(destination_list) == 2 and all([isinstance(float(x), float) for x in destination_list])):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Destination is not a valid values or not separated by comma"
            return
        allowed_distance = frappe.get_single("Mohan Impex Settings").allowed_distance
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={api_key}"
        response = requests.get(url).json()
        
        if response["status"] == "OK":
            if not response["rows"][0]["elements"][0]["status"] == "OK":
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['status'] = False
                frappe.local.response['message'] = "No Address found for the given Orgin or Destination"
                return
            distance_meters = response["rows"][0]["elements"][0]["distance"]["value"]  # Distance in meters
            valid_distance = distance_meters <= allowed_distance
            response = {
                "valid": valid_distance, 
                "distance": distance_meters,
            }
            message = "You are within the range to submit the visit" if valid_distance else f"You are {int(allowed_distance)} meters away from the origin to submit the visit"
            response.update({"message": message})
            frappe.local.response['status'] = True
            frappe.local.response['message'] = "Validation of distance for the range has been done"
            frappe.local.response['data'] = response
            return
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Issue with LOCATION or API_KEY"
        frappe.local.response['data'] = response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = f"{err}"

def get_role_filter(emp, is_self=None, employee=None):
    territory_list = set(frappe.get_all("User Permission", {"allow": "Territory", "user": emp.get("user_id")}, ["for_value as area"], pluck="area"))
    consolidated_territory = set(territory_list)
    for area in territory_list:
        consolidated_territory.update(get_descendants_of("Territory", area))
    areas = "', '".join(consolidated_territory) if consolidated_territory else f"""{emp.get("area")}"""
    if employee:
        return f"""area in ('{areas}') and created_by_emp = '{employee}' """
    if is_self is not None:
        if int(is_self) == 1:
            return f"""area in ('{areas}') and created_by_emp = '{emp.get('name')}' """
        elif int(is_self) == 0:
            return f"""area in ('{areas}') and (created_by_emp != '{emp.get('name')}' or created_by_emp is null) """
    return f"""area in ('{areas}') """

def get_territory_role_filter(emp):
    # territory_list = emp.get("multiple_areas", []) if emp.get("is_multiple_area_management") else [emp]
    # territory_list = [area.get("area") for area in territory_list]
    user = frappe.session.user
    territory_list = set(frappe.get_all("User Permission", {"allow": "Territory", "user": user}, ["for_value as area"], pluck="area"))
    consolidated_territory = set(territory_list)
    for area in territory_list:
        consolidated_territory.update(get_descendants_of("Territory", area))
    areas = "', '".join(consolidated_territory) if consolidated_territory else f"""{emp.get("area")}"""
    return f"""territory in ('{areas}') """

def get_self_filter_status():
    role_profile = frappe.get_value("Employee", {"user_id": frappe.session.user}, "role_profile")
    return frappe.db.get_value("Role Profile", role_profile, "has_toggle_filter")

@frappe.whitelist()
def get_sales_invoices(customer):
    sales_invoices = frappe.get_all("Sales Invoice", {"customer": customer, "docstatus": ["!=", 2]}, ["name", "posting_date as date"])
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Sales Invoice list has been fetched successfully"
    frappe.local.response['data'] = sales_invoices

@frappe.whitelist()
def get_sales_invoice_items(sales_invoice):
    si_items = frappe.get_all("Sales Invoice Item", {"parent": sales_invoice}, ["item_code", "item_name", "qty", "amount"])
    frappe.local.response['status'] = True
    frappe.local.response['message'] = "Sales Invoice Items has been fetched successfully"
    frappe.local.response['data'] = si_items

def get_address_text(address_name):
    addr_doc = frappe.get_doc("Address", address_name)
    address_text = ""
    address_text += f"{addr_doc.address_line1}, " if addr_doc.address_line1 else ""
    address_text += f"{addr_doc.address_line2}, " if addr_doc.address_line2 else ""
    address_text += f"{addr_doc.district}, " if addr_doc.district else ""
    address_text += f"{addr_doc.state}, " if addr_doc.state else ""
    address_text += f"{addr_doc.pincode}" if addr_doc.pincode else ""
    return address_text

@frappe.whitelist()
def get_employee_list(area, role_profile=None):
    session_emp = get_session_employee()
    sub_areas = get_descendants_of("Territory", area) or []
    sub_areas.append(area)
    try:
        filters = {
            "area": ["in", sub_areas],
            "status": "Active",
            "name": ["!=", session_emp]
        }
        if role_profile:
            filters["role_profile"] = role_profile
        employee_list = frappe.get_all("Employee", filters, ["name", "employee_name"])
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Employee List has been fetched successfully"
        frappe.local.response['data'] = employee_list
    except Exception as err:
        get_exception(err)
    
def get_exception(err):
    frappe.local.response['http_status_code'] = 404
    frappe.local.response['status'] = False
    if len(frappe.local.message_log) > 0:
        err = frappe.local.message_log[0].get("message") or err
    soup = BeautifulSoup(err, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with(". ")
    err = soup.get_text()
    frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

def get_workflow_statuses(doctype, doc_name, role):
    doc = frappe.get_doc(doctype, doc_name)
    workflow_statuses = get_transitions(doc)
    workflow_statuses = list(filter(lambda workflow: workflow["allowed"] == role, workflow_statuses))
    workflow_statuses = [workflow["action"] for workflow in workflow_statuses]
    return workflow_statuses

def has_create_perm(doctype):
    return 1 if frappe.has_permission(doctype, "create", user=frappe.session.user) else 0


# def add_notification_from_assignment(doc, method):
    # doctype_lists = ["Trial Plan"]
    # try:
    #     if doc.reference_type in doctype_lists:
    #         assigned_by = doc.assigned_by_full_name
    #         assigned_to = doc.allocated_to
    #         title = f"{doc.reference_type} has been assigned to you"
    #         body = f"{doc.reference_type} {doc.reference_name} has been assigned to you by {assigned_by}" 
    #         create_notification_log(doc, [assigned_to], title, body)
    # except Exception as e:
    #     frappe.log_error(message=frappe.get_traceback(), title="Notification Log from Assignment Error")

def add_notification_from_comment(doc, method):
    doctype_lists = ["Customer Visit Management", "Trial Plan", "Sample Requisition", "Sales Order", "Issue", "Marketing Collateral Request", "Customer", "Journey Plan"]
    try:
        if doc.reference_doctype in doctype_lists and doc.get("comment_type") in ["Comment", "Workflow"]:
            owner = frappe.get_value(doc.reference_doctype, doc.reference_name, "owner")
            role, area = frappe.get_value("Employee", {"user_id": owner}, ["role_profile", "area"])
            parent_areas = get_parent_areas(area)
            sales_team = ["SE", "ASM", "TSM", "NSM", "ZSM", "RSM"]
            notification_users = frappe.get_all("Employee", {"area": ["in", parent_areas], "role_profile": ["in", sales_team]}, pluck = "user_id") or []
            # Check for the User who has permission for the record (Specifically for TSM)
            if not frappe.has_permission(doc.reference_doctype, "read", doc.reference_name, user=owner):
                notification_users.remove(owner)
            comment_owner = doc.owner
            notification_users.insert(0, owner)
            if comment_owner in notification_users:
                notification_users.remove(comment_owner)
            if doc.get("comment_type") == "Workflow":
                title = f"{doc.reference_doctype} status has been updated"
                body = f"{doc.reference_doctype} {doc.reference_name} status has been updated by {doc.comment_by} to {doc.content}"
            elif doc.get("comment_type") == "Comment":
                title = f"{doc.comment_by} commented in {doc.reference_doctype}"
                soup = BeautifulSoup(doc.content, "html.parser")
                body = soup.get_text(separator=" ")
            create_notification_log(doc, notification_users, title, body)
    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Notification Log from Comment Error")

def create_notification_log(doc, users_list, title, body):
    for user in users_list:
        notify_doc = frappe.new_doc("Notification Log")
        notify_doc.update({
            "for_user": user,
            "read": 0,
            "subject": title,
            "email_content": body,
            "document_type" : doc.reference_doctype,
            "document_name": doc.reference_name
        })
        notify_doc.insert(ignore_permissions=True)

def get_parent_areas(area):
    parent_areas = []
    current_area = area
    while current_area:
        parent_area = frappe.get_value("Territory", current_area, "parent_territory")
        if parent_area:
            parent_areas.append(parent_area)
            current_area = parent_area
        else:
            break
    return parent_areas

def send_notification(doc, method):
    doctype_lists = ["Customer Visit Management", "Trial Plan", "Sample Requisition", "Sales Order", "Issue", "Marketing Collateral Request", "Customer", "Journey Plan"]
    if doc.document_type in doctype_lists and doc.type in ("", "Assignment"):
        role_profile = frappe.get_value("User", doc.for_user, "role_profile_name")
        if doc.for_user and doc.for_user != "Administrator":
            device_tokens = frappe.get_all("Push Notification Device", filters={"user": doc.for_user, "disabled": 0}, pluck="device_token")
            soup = BeautifulSoup(doc.subject, "html.parser")
            title = soup.get_text(separator=" ")
            body = doc.email_content
            data = {
                "type": doc.document_type,
                "id": doc.document_name,
                "role_profile": role_profile
            }
            for device_token in device_tokens:
                send_push_notification(doc.for_user, device_token, title, body, data)

@frappe.whitelist()
def send_push_notification(for_user, device_token, title, body, data=None):
    service_account_path = 'mohan-impex-erp-551f3-1f9a5f51dd38.json'

    project_id = 'mohan-impex-erp-551f3'

    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

    # Authenticate and get access token
    credentials = service_account.Credentials.from_service_account_file(
        service_account_path, scopes=SCOPES)
    credentials.refresh(Request())
    access_token = credentials.token

    # Prepare the notification payload
    payload = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    if data:
        if isinstance(data, str):
            data = json.loads(data)
        payload["message"]["data"] = data  # Optional custom data

    # Send request to FCM
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8"
    }

    try:
        pnl_log = frappe.new_doc("Push Notification Log")
        log_dict = {
            "user": for_user,
            "device_token": device_token,
            "payload": json.dumps(payload, indent=4),
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            frappe.local.response["status"] = True 
            frappe.local.response["message"] = response.json()
            log_dict.update({
                "error_text": response.text,
                "status": "Sent"
            })
        else:
            if response.status_code == 404 and "UNREGISTERED" in response.text:
                frappe.db.set_value("Push Notification Device", {"device_token": device_token}, "disabled", 1)
            log_dict.update({
                "error_text": response.text,
                "status": "Error"
            })
            frappe.local.response["status"] = False
            frappe.local.response["message"] = response.json()
        pnl_log.update(log_dict)
        pnl_log.insert(ignore_permissions=True)
    except Exception as err:
        pnl_log = frappe.new_doc("Push Notification Log")
        pnl_log.update({
            "user": for_user,
            "device_token": device_token,
            "payload": json.dumps(payload, indent=4),
            "error_text": str(err),
            "status": "Error"
        })
        pnl_log.insert(ignore_permissions=True)
        get_exception(err)

def convert_to_12_hour(db_time):
    db_time = (datetime.min + db_time).time()
    time_str = str(db_time)
    if "." in time_str:
        time_str = time_str.split(".")[0]
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    return time_obj.strftime("%I:%M:%S %p")