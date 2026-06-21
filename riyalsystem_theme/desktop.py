import frappe
from frappe import _
from frappe.desk.desktop import Workspace


def _apply_workspace_menu_display(page):
	custom_title = page.get("custom_menu_title")
	if custom_title:
		page["label"] = custom_title
		page["title"] = custom_title
	elif not page.get("label"):
		page["label"] = page.get("title") or page.get("name")


@frappe.whitelist()
def get_workspace_sidebar_items():
	"""Return workspace sidebar pages including theme custom fields."""
	has_access = "Workspace Manager" in frappe.get_roles()

	blocked_modules = frappe.get_cached_doc("User", frappe.session.user).get_blocked_modules()
	blocked_modules.append("Dummy Module")

	allowed_domains = [None, *frappe.get_active_domains()]

	filters = {
		"restrict_to_domain": ["in", allowed_domains],
		"module": ["not in", blocked_modules],
	}

	if has_access:
		filters = []

	order_by = "sequence_id asc"
	fields = [
		"name",
		"title",
		"custom_default_dashboard",
		"custom_open_dashboard",
		"custom_menu_title",
		"custom_hide_from_menu",
		"for_user",
		"parent_page",
		"content",
		"public",
		"module",
		"icon",
		"indicator_color",
		"is_hidden",
	]
	all_pages = frappe.get_all(
		"Workspace", fields=fields, filters=filters, order_by=order_by, ignore_permissions=True
	)
	pages = []
	private_pages = []

	for page in all_pages:
		if frappe.utils.cint(page.get("custom_hide_from_menu")):
			continue

		try:
			workspace = Workspace(page, True)
			if has_access or workspace.is_permitted():
				_apply_workspace_menu_display(page)
				if page.public and (has_access or not page.is_hidden) and page.title != "Welcome Workspace":
					pages.append(page)
				elif page.for_user == frappe.session.user:
					private_pages.append(page)
				page["label"] = _(page.get("custom_menu_title") or page.get("title") or page.get("name"))
		except frappe.PermissionError:
			pass

	if private_pages:
		pages.extend(private_pages)

	if len(pages) == 0:
		pages = [frappe.get_doc("Workspace", "Welcome Workspace").as_dict()]
		pages[0]["label"] = _("Welcome Workspace")

	return {
		"pages": pages,
		"has_access": has_access,
		"has_create_access": frappe.has_permission(doctype="Workspace", ptype="create"),
	}
