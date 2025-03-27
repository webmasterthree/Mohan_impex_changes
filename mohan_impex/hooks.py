app_name = "mohan_impex"
app_title = "Mohan Impex"
app_publisher = "Edubild"
app_description = "Mohan Impex"
app_email = "arunlrajamanickam@gmail.com"
app_license = "mit"


fixtures = [
    "Client Script",
    {"dt": "Custom DocPerm", "filters": [["role", "in", ("SE", "ASM", "TSM", "NSM")]]},
    {"dt": "Property Setter", "filters": [["doc_type", "in", ("Customer")], ["property", "in", "options"]]},
    {"dt": "Role", "filters": [["name", "in", ("SE", "ASM", "TSM", "NSM")]]},
    {"dt": "Role Profile", "filters": [["name", "in", ("SE", "ASM", "TSM", "NSM")]]},
    {"dt": "Designation", "filters": [["name", "in", ("SE", "ASM", "TSM", "NSM")]]},
    {"dt": "Module Profile", "filters": [["name", "in", ("Mohan Impex")]]},
    {"dt": "Workspace", "filters": [["name", "in", ("Mohan Impex")]]},
    "Workflow",
    "Workflow State",
    "Workflow Action Master"
]

doctype_js ={
    "Sales Order": "public/js/sales_order.js",
    "Purchase Order" : "public/js/purchase_order.js",
    "Employee":"public/js/employee.js",
    "Request for Quotation": "public/js/request_for_quotation.js",
    "Additional Salary": "public/js/additional_salary.js",
    "Request for Quotation" : "public/js/rfq.js",
    "Pre-Unloading Check": "public/js/pre_unloading_check.js",
    "User": "public/js/user.js",
    "Sales Order":"public/js/outstanding_amount.js",
}
# "Purchase Receipt":"public/js/PR_Connection.js",
# "Purchase Receipt":"public/js/GRN1_Item.js",

doc_events = {
	"Comment": {
		"after_insert": "mohan_impex.mohan_impex.comment.status_update"
	},
    "Sales Order": {
        "before_save": "mohan_impex.mohan_impex.sales_order.update_customer_edit_needed"
    },
    "Employee": {
        "before_save": "mohan_impex.mohan_impex.employee.set_user_permissions"
    },
    "Customer": {
        "before_save": "mohan_impex.mohan_impex.customer.validate_dup_unv_id",
        "after_insert": "mohan_impex.mohan_impex.customer.updated_workflow_state"
    },
    "Request for Quotation": {
        "on_submit": "mohan_impex.rfq.send_rfq_email"
    },
    "Employee Checkin": {
        "before_save": "mohan_impex.leave_deduction.before_save_employee_checkin"
    },
    "Transport RFQ": {
        "on_submit": "mohan_impex.Sales.Assign_Transporter.on_submit"
    },
    "Salary Slip": {
        "on_submit": "mohan_impex.salary_slip.handle_pf_on_submit"
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
# scheduler_events = {
#     "hourly": [
#         "mohan_impex.auto_close_rfq.close_expired_rfqs"
#     ]
# }
scheduler_events = {
    "cron": {
        "15 12 * * *": [
            "mohan_impex.auto_close_rfq.close_expired_rfqs"
        ]
    },
    "monthly":[
        "mohan_impex.leave_balance.allocate_monthly_leave"
    ],
}

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
#

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

