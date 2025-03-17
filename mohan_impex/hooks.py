app_name = "mohan_impex"
app_title = "Mohan Impex"
app_publisher = "Edubild"
app_description = "Mohan Impex"
app_email = "arunlrajamanickam@gmail.com"
app_license = "mit"


# fixtures = [
#     "Client Script"
# ]

doctype_js ={
    "Sales Order": "public/js/sales_order.js",
    "Purchase Order" : "public/js/purchase_order.js",
    "Employee":"public/js/employee.js",
    "Request for Quotation": "public/js/request_for_quotation.js",
    "Additional Salary": "public/js/additional_salary.js",
    "Request for Quotation" : "public/js/rfq.js",
    "Request for Quotation" : "public/js/rfq_supplier.js",
    "Pre-Unloading Check": "public/js/pre_unloading_check.js",
    "User": "public/js/user.js",

}
doc_events = {
    "Request for Quotation": {
        "on_submit": "mohan_impex.rfq.send_rfq_email"
    }
}

doc_events = {
    # Trigger before saving Employee Checkin to check late entries and create leave if necessary
    "Employee Checkin": {
        "before_save": "mohan_impex.leave_deduction.before_save_employee_checkin"
    }
}


# Whitelist API methods for external use
api_methods = [
    "mohan_impex.leave_deduction.create_casual_leave"
]



# doctype_js = {
#     "BOM": "public/js/bom.js"
# }

# 
# api = {
#     "methods": [
#         "mohan_impex.api.download_attendance_report"
#     ]
# }

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "mohan_impex",
# 		"logo": "/assets/mohan_impex/logo.png",
# 		"title": "Mohan Impex",
# 		"route": "/mohan_impex",
# 		"has_permission": "mohan_impex.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mohan_impex/css/mohan_impex.css"
# app_include_js = "/assets/mohan_impex/js/mohan_impex.js"

# include js, css files in header of web template
# web_include_css = "/assets/mohan_impex/css/mohan_impex.css"
# web_include_js = "/assets/mohan_impex/js/mohan_impex.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mohan_impex/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mohan_impex/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mohan_impex.utils.jinja_methods",
# 	"filters": "mohan_impex.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mohan_impex.install.before_install"
# after_install = "mohan_impex.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mohan_impex.uninstall.before_uninstall"
# after_uninstall = "mohan_impex.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mohan_impex.utils.before_app_install"
# after_app_install = "mohan_impex.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mohan_impex.utils.before_app_uninstall"
# after_app_uninstall = "mohan_impex.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mohan_impex.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mohan_impex.tasks.all"
# 	],
# 	"daily": [
# 		"mohan_impex.tasks.daily"
# 	],
# 	"hourly": [
# 		"mohan_impex.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mohan_impex.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mohan_impex.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "mohan_impex.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mohan_impex.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mohan_impex.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mohan_impex.utils.before_request"]
# after_request = ["mohan_impex.utils.after_request"]

# Job Events
# ----------
# before_job = ["mohan_impex.utils.before_job"]
# after_job = ["mohan_impex.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mohan_impex.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

