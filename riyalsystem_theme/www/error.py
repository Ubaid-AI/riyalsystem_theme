# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe
from frappe import _
from frappe.utils.response import is_traceback_allowed

from riyalsystem_theme.www.theme_context import get_web_theme_context

no_cache = 1


def get_context(context):
	if frappe.flags.in_migrate:
		return

	context.error_title = context.error_title or _("Uncaught Server Exception")
	context.error_message = context.error_message or _("There was an error building this page")

	context.update(get_web_theme_context())
	return {
		"error": frappe.get_traceback().replace("<", "&lt;").replace(">", "&gt;")
		if is_traceback_allowed()
		else ""
	}
