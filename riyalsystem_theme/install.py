# Copyright (c) 2025, Riyalsystem Theme

import frappe

from riyalsystem_theme.saudi_riyal import apply_saudi_riyal_symbol
from riyalsystem_theme.workspace_process_flows.workspace_links import (
	sync_workspace_assignments,
)


def after_install():
	"""Apply theme patches when the app is installed on a site."""
	_apply_patches("after_install")


def after_migrate():
	"""Re-apply idempotently after migrate."""
	_apply_patches("after_migrate")


def _apply_patches(source: str) -> None:
	_apply_saudi_riyal_symbol(source)
	_apply_workspace_blocks(source)


def _apply_saudi_riyal_symbol(source: str) -> None:
	try:
		result = apply_saudi_riyal_symbol()
		if result["currency_updated"] or result["print_style_updated"]:
			frappe.logger("riyalsystem_theme").info(
				f"Saudi Riyal symbol patch applied via {source}: {result}"
			)
	except Exception:
		frappe.log_error(
			title="Saudi Riyal symbol patch failed",
			message=frappe.get_traceback(),
		)


def _apply_workspace_blocks(source: str) -> None:
	try:
		results = sync_workspace_assignments()
		if any(item.get("updated") for item in results):
			frappe.logger("riyalsystem_theme").info(
				f"Workspace process-flow blocks synced via {source}: {results}"
			)
	except Exception:
		frappe.log_error(
			title="Workspace process-flow block sync failed",
			message=frappe.get_traceback(),
		)
