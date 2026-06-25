# Copyright (c) 2025, Riyalsystem Theme

import frappe

from riyalsystem_theme.saudi_riyal import apply_saudi_riyal_symbol


def after_install():
	"""Apply Saudi Riyal symbol support when the theme app is installed."""
	_apply_patch("after_install")


def after_migrate():
	"""Re-apply idempotently after migrate (covers late Currency/Print Style creation)."""
	_apply_patch("after_migrate")


def _apply_patch(source: str) -> None:
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
