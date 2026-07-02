# Copyright (c) 2025, Riyalsystem Theme
"""Apply Saudi Riyal symbol patch (§ + Cairo Saudi font in Modern print style)."""

from __future__ import annotations

import frappe

PRINT_STYLE_NAME = "Modern"
CURRENCY_NAME = "SAR"
# Section sign used as placeholder; Cairo Saudi font renders the new Riyal glyph for U+00A7.
RIYAL_SYMBOL = "\u00a7"
PATCH_MARKER = "Cairo Saudi"


def get_modern_print_style_css() -> str:
	path = frappe.get_app_path(
		"riyalsystem_theme", "data", "modern_print_style_saudi_riyal.css"
	)
	with open(path, encoding="utf-8") as handle:
		return handle.read()


def apply_saudi_riyal_symbol(force: bool = False) -> dict:
	"""Update SAR currency symbol and Modern Print Style CSS.

	Returns a summary dict for logging / bench output.
	"""
	result = {
		"currency_updated": False,
		"print_style_updated": False,
		"print_settings_updated": False,
		"skipped": [],
	}

	if frappe.db.exists("Currency", CURRENCY_NAME):
		current_symbol = frappe.db.get_value("Currency", CURRENCY_NAME, "symbol")
		if force or current_symbol != RIYAL_SYMBOL:
			frappe.db.set_value(
				"Currency",
				CURRENCY_NAME,
				"symbol",
				RIYAL_SYMBOL,
				update_modified=False,
			)
			result["currency_updated"] = True
	else:
		result["skipped"].append(f"Currency {CURRENCY_NAME} not found")

	if frappe.db.exists("Print Style", PRINT_STYLE_NAME):
		css = get_modern_print_style_css()
		current_css = frappe.db.get_value("Print Style", PRINT_STYLE_NAME, "css") or ""
		if force or PATCH_MARKER not in current_css or current_css.strip() != css.strip():
			_update_print_style_css(css)
			result["print_style_updated"] = True
	else:
		result["skipped"].append(f"Print Style {PRINT_STYLE_NAME} not found")

	_update_print_settings_print_style(force=force, result=result)

	if (
		result["currency_updated"]
		or result["print_style_updated"]
		or result["print_settings_updated"]
	):
		frappe.db.commit()
		frappe.clear_cache(doctype="Currency")
		frappe.clear_cache(doctype="Print Style")
		frappe.clear_cache(doctype="Print Settings")

	return result


def _update_print_style_css(css: str) -> None:
	"""Persist CSS on the standard Modern print style."""
	frappe.flags.in_import = True
	try:
		doc = frappe.get_doc("Print Style", PRINT_STYLE_NAME)
		doc.css = css
		doc.flags.ignore_permissions = True
		doc.save(ignore_permissions=True)
	finally:
		frappe.flags.in_import = False


def _update_print_settings_print_style(*, force: bool, result: dict) -> None:
	"""Ensure Print Settings uses the Modern print style for SAR symbol rendering."""
	if not frappe.db.exists("Print Style", PRINT_STYLE_NAME):
		result["skipped"].append(f"Print Settings not updated; {PRINT_STYLE_NAME} missing")
		return

	current_style = frappe.db.get_single_value("Print Settings", "print_style")
	if not force and current_style == PRINT_STYLE_NAME:
		return

	frappe.db.set_single_value(
		"Print Settings",
		"print_style",
		PRINT_STYLE_NAME,
		update_modified=False,
	)
	result["print_settings_updated"] = True
