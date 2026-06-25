# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

from riyalsystem_theme.www.theme_context import get_web_theme_context


def get_context(context):
	context.http_status_code = 404
	context.update(get_web_theme_context())
	return context
