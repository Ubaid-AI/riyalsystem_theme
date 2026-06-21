/*
 * Normalized Theme Settings checkbox helpers.
 */
(function () {
	'use strict';

	function as_theme_bool(value) {
		if (value === true || value === 1 || value === '1') {
			return true;
		}
		if (value === false || value === 0 || value === '0' || value == null || value === '') {
			return false;
		}
		if (typeof value === 'string') {
			const normalized = value.trim().toLowerCase();
			if (normalized === 'true' || normalized === 'yes') {
				return true;
			}
			if (normalized === 'false' || normalized === 'no') {
				return false;
			}
		}
		return !!parseInt(value, 10);
	}

	function as_theme_check(value) {
		return as_theme_bool(value) ? 1 : 0;
	}

	function as_theme_check_str(value) {
		return as_theme_check(value) ? '1' : '0';
	}

	function normalize_theme_settings(settings) {
		settings = Object.assign({}, settings || {});
		const check_fields = [
			'show_icon_label',
			'hide_icon_tooltip',
			'always_close_sub_menu',
			'apply_on_navbar',
			'apply_on_menu',
			'apply_on_dashboard',
			'apply_on_workspace',
			'apply_dark_mode',
			'dark_view',
			'hide_language_icon',
			'show_help_icon',
			'open_workspace_on_mobile_menu',
		];

		check_fields.forEach(function (field) {
			if (field in settings) {
				settings[field] = as_theme_check(settings[field]);
			}
		});

		return settings;
	}

	frappe.provide('riyalsystem_theme');
	riyalsystem_theme.as_theme_bool = as_theme_bool;
	riyalsystem_theme.as_theme_check = as_theme_check;
	riyalsystem_theme.as_theme_check_str = as_theme_check_str;
	riyalsystem_theme.normalize_theme_settings = normalize_theme_settings;
})();
