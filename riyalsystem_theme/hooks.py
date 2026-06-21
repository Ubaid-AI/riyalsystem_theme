from . import __version__ as app_version

app_name = "riyalsystem_theme"
app_title = "Riyalsystem Theme"
app_publisher = "Abdo Hamoud"
app_description = "Frappe 15 Theme App"
app_email = "abdo.host@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

website_context = {
    "favicon": "/assets/riyalsystem_theme/images/datavlue-new-icon-xs.png",
    "splash_image": "/assets/riyalsystem_theme/images/theme_splash_empty.jpg"
}

app_include_css = [
    "/assets/riyalsystem_theme/plugins/animate.css/animate.min.css",
    "/assets/riyalsystem_theme/plugins/fontawesome/all.min.css",
    "/assets/riyalsystem_theme/plugins/tooltip/tooltip-theme-twipsy.css",
    "/assets/riyalsystem_theme/plugins/flat-icons/flaticon.css",
    "/assets/riyalsystem_theme/plugins/simple-calendar/simple-calendar.css",
    "datavalue_theme.bundle.css"
]

app_include_js = [
    "/assets/riyalsystem_theme/plugins/vue/vue.js",
    "/assets/riyalsystem_theme/plugins/bootstrap4c-chosen/chosen.min.js",
    "/assets/riyalsystem_theme/plugins/nicescroll/nicescroll.js",
    "/assets/riyalsystem_theme/plugins/tooltip/tooltip.js",
    "/assets/riyalsystem_theme/plugins/jquery-fullscreen/jquery.fullscreen.min.js?ver=1",
    "/assets/riyalsystem_theme/plugins/simple-calendar/jquery.simple-calendar.js",
    "/assets/riyalsystem_theme/js/datavalue_theme.app.min.js"
    # "datavalue_theme.bundle.js"
]

email_brand_image = "assets/riyalsystem_theme/images/logo-v.png"

# include js, css files in header of web template
web_include_css = [
    "assets/riyalsystem_theme/plugins/fontawesome/all.min.css",
    "assets/riyalsystem_theme/css/login.css",
    "assets/riyalsystem_theme/css/dv-login.css?ver=" + app_version
]
web_include_js = [
    "/assets/riyalsystem_theme/js/datavalue_theme.web.min.js?ver=" + app_version
]

# include js, css files in header of desk.html
# app_include_css = "/assets/riyalsystem_theme/css/riyalsystem_theme.css"
# app_include_js = "/assets/riyalsystem_theme/js/riyalsystem_theme.js"

# include js, css files in header of web template
# web_include_css = "/assets/riyalsystem_theme/css/riyalsystem_theme.css"
# web_include_js = "/assets/riyalsystem_theme/js/riyalsystem_theme.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "riyalsystem_theme/public/scss/website"

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
# app_include_icons = "riyalsystem_theme/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "riyalsystem_theme.utils.jinja_methods",
#	"filters": "riyalsystem_theme.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "riyalsystem_theme.install.before_install"
# after_install = "riyalsystem_theme.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "riyalsystem_theme.uninstall.before_uninstall"
# after_uninstall = "riyalsystem_theme.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "riyalsystem_theme.utils.before_app_install"
# after_app_install = "riyalsystem_theme.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "riyalsystem_theme.utils.before_app_uninstall"
# after_app_uninstall = "riyalsystem_theme.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "riyalsystem_theme.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"riyalsystem_theme.tasks.all"
#	],
#	"daily": [
#		"riyalsystem_theme.tasks.daily"
#	],
#	"hourly": [
#		"riyalsystem_theme.tasks.hourly"
#	],
#	"weekly": [
#		"riyalsystem_theme.tasks.weekly"
#	],
#	"monthly": [
#		"riyalsystem_theme.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "riyalsystem_theme.install.before_tests"

# Overriding Methods
# ------------------------------
override_whitelisted_methods = {
	"frappe.desk.desktop.get_workspace_sidebar_items": "riyalsystem_theme.desktop.get_workspace_sidebar_items",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "riyalsystem_theme.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["riyalsystem_theme.utils.before_request"]
# after_request = ["riyalsystem_theme.utils.after_request"]

# Job Events
# ----------
# before_job = ["riyalsystem_theme.utils.before_job"]
# after_job = ["riyalsystem_theme.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"riyalsystem_theme.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
#	"Logging DocType Name": 30  # days to retain logs
# }

# Fixtures
# --------

fixtures = [
	{
		"dt": "Custom HTML Block",
		"filters": [
			[
				"name",
				"in",
				[
					"RST Selling Process Flow",
					"RST Buying Process Flow",
					"RST CRM Process Flow",
					"RST Stock Process Flow",
					"RST Manufacturing Process Flow",
					"RST Accounting Process Flow",
					"RST Projects Process Flow",
					"RST HR Process Flow",
					"RST Support Process Flow",
					"RST Quality Process Flow",
					"RST Assets Process Flow",
				],
			]
		],
	},
]

after_migrate = [
	"riyalsystem_theme.workspace_process_flows.sync.sync_blocks",
]
