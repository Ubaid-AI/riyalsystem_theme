/*
 * Apply Dark Mode from Theme Settings (apply_dark_mode + legacy dark_view)
 */
(function () {
	'use strict';

	function cint(value) {
		return parseInt(value, 10) || 0;
	}

	function get_settings() {
		return frappe.theme_settings || {};
	}

	function is_dark_mode_enabled(settings) {
		settings = settings || get_settings();
		return cint(settings.apply_dark_mode) || cint(settings.dark_view);
	}

	function color_class_name(color) {
		return 'dv-' + String(color || 'Blue').replace(/ /g, '-') + '-style';
	}

	function sync_layout_classes(settings) {
		settings = settings || get_settings();
		const $body = $('body');

		$body.toggleClass('layout-navbar-color-style', cint(settings.apply_on_navbar));
		$body.toggleClass('layout-menu-color-style', cint(settings.apply_on_menu));
		$body.toggleClass('layout-dashboard-color-style', cint(settings.apply_on_dashboard));
		$body.toggleClass('layout-workspace-color-style', cint(settings.apply_on_workspace));
	}

	function sync_color_class(settings) {
		settings = settings || get_settings();
		const color = settings.theme_color || $('body').attr('data-theme-colorname') || 'Blue';
		const next_class = color_class_name(color);
		const $body = $('body');
		const classes = ($body.attr('class') || '').split(/\s+/);

		classes.forEach(function (cls) {
			if (cls.indexOf('dv-') === 0 && cls.indexOf('-style') === cls.length - 6) {
				$body.removeClass(cls);
			}
		});
		$body.addClass(next_class);
		$body.attr('data-theme-colorname', color);
	}

	function apply_dark_mode_to_page(enabled) {
		const is_dark = cint(enabled);
		const theme = is_dark ? 'dark' : 'light';
		const $body = $('body');
		const $html = $('html');

		$body.toggleClass('dv-dark-style', !!is_dark);
		$body.toggleClass('dv-theme-dark', !!is_dark).toggleClass('dv-theme-light', !is_dark);
		$html.attr('data-theme', theme).attr('data-theme-mode', theme).attr('data-dv-theme', theme);
		document.documentElement.setAttribute('data-theme', theme);
		document.documentElement.setAttribute('data-theme-mode', theme);
	}

	function apply_theme_settings_to_page(settings) {
		settings = settings || get_settings();
		sync_color_class(settings);
		sync_layout_classes(settings);
		apply_dark_mode_to_page(is_dark_mode_enabled(settings));
	}

	function sync_dark_mode_from_settings() {
		apply_theme_settings_to_page(get_settings());
	}

	$(document).ready(sync_dark_mode_from_settings);
	$(document).one('app-loaded', sync_dark_mode_from_settings);
	$(document).one('dv-app-loaded', sync_dark_mode_from_settings);

	frappe.provide('riyalsystem_theme');
	riyalsystem_theme.apply_dark_mode_to_page = apply_dark_mode_to_page;
	riyalsystem_theme.apply_theme_settings_to_page = apply_theme_settings_to_page;
	riyalsystem_theme.is_dark_mode_enabled = is_dark_mode_enabled;
	riyalsystem_theme.sync_layout_classes = sync_layout_classes;
})();
