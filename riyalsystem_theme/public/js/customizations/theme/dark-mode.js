/*
 * Apply Theme Settings to the desk page (colors, layout gates, dark mode, side menu).
 */
(function () {
	'use strict';

	function as_theme_bool(value) {
		return frappe.riyalsystem_theme && frappe.riyalsystem_theme.as_theme_bool
			? frappe.riyalsystem_theme.as_theme_bool(value)
			: !!(parseInt(value, 10) || value === true);
	}

	function as_theme_check(value) {
		return frappe.riyalsystem_theme && frappe.riyalsystem_theme.as_theme_check
			? frappe.riyalsystem_theme.as_theme_check(value)
			: as_theme_bool(value) ? 1 : 0;
	}

	function normalize_settings(settings) {
		if (frappe.riyalsystem_theme && frappe.riyalsystem_theme.normalize_theme_settings) {
			return frappe.riyalsystem_theme.normalize_theme_settings(settings);
		}
		return settings || {};
	}

	function get_settings() {
		return normalize_settings(frappe.theme_settings || {});
	}

	function is_dark_mode_enabled(settings) {
		settings = settings || get_settings();
		return as_theme_bool(settings.apply_dark_mode) || as_theme_bool(settings.dark_view);
	}

	function color_class_name(color) {
		return 'dv-' + String(color || 'Blue').replace(/ /g, '-') + '-style';
	}

	function sync_layout_classes(settings) {
		settings = settings || get_settings();
		const $body = $('body');

		$body.toggleClass('layout-navbar-color-style', as_theme_bool(settings.apply_on_navbar));
		$body.toggleClass('layout-menu-color-style', as_theme_bool(settings.apply_on_menu));
		$body.toggleClass('layout-dashboard-color-style', as_theme_bool(settings.apply_on_dashboard));
		$body.toggleClass('layout-workspace-color-style', as_theme_bool(settings.apply_on_workspace));
	}

	function as_theme_check_str(value) {
		return frappe.riyalsystem_theme && frappe.riyalsystem_theme.as_theme_check_str
			? frappe.riyalsystem_theme.as_theme_check_str(value)
			: as_theme_check(value) ? '1' : '0';
	}

	function sync_side_menu_checkbox_effects(settings) {
		settings = settings || get_settings();
		const $icons = $('.side-menu .side-menu-icons');
		if (!$icons.length) {
			return;
		}

		const show_label = as_theme_bool(settings.show_icon_label);
		$icons.toggleClass('menu-icons-with-label', show_label);

		const tooltip_mode = as_theme_bool(settings.hide_icon_tooltip) ? '' : 'tipsy';
		$icons.find('> ul > li > a').attr('data-toggle', tooltip_mode);

		const menu_vm = document.getElementById('side-menu-component')?.__vue_app__?._instance?.proxy;
		if (menu_vm && menu_vm.theme_settings) {
			menu_vm.theme_settings.show_icon_label = as_theme_check_str(settings.show_icon_label);
			menu_vm.theme_settings.hide_icon_tooltip = as_theme_check_str(settings.hide_icon_tooltip);
		}
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
		const is_dark = as_theme_bool(enabled);
		const theme = is_dark ? 'dark' : 'light';
		const $body = $('body');
		const $html = $('html');

		$body.toggleClass('dv-dark-style', is_dark);
		$body.toggleClass('dv-theme-dark', is_dark).toggleClass('dv-theme-light', !is_dark);
		$html.attr('data-theme', theme).attr('data-theme-mode', theme).attr('data-dv-theme', theme);
		document.documentElement.setAttribute('data-theme', theme);
		document.documentElement.setAttribute('data-theme-mode', theme);
	}

	function apply_theme_settings_to_page(settings) {
		settings = normalize_settings(settings || frappe.theme_settings || {});
		frappe.theme_settings = Object.assign(frappe.theme_settings || {}, settings);
		sync_color_class(settings);
		sync_layout_classes(settings);
		sync_side_menu_checkbox_effects(settings);
		apply_dark_mode_to_page(is_dark_mode_enabled(settings));
	}

	function sync_dark_mode_from_settings() {
		apply_theme_settings_to_page(get_settings());
	}

	$(document).ready(sync_dark_mode_from_settings);
	$(document).one('app-loaded', sync_dark_mode_from_settings);
	$(document).one('app-loaded', function () {
		setTimeout(sync_dark_mode_from_settings, 1500);
	});
	$(document).one('dv-app-loaded', sync_dark_mode_from_settings);

	frappe.provide('riyalsystem_theme');
	riyalsystem_theme.apply_dark_mode_to_page = apply_dark_mode_to_page;
	riyalsystem_theme.apply_theme_settings_to_page = apply_theme_settings_to_page;
	riyalsystem_theme.is_dark_mode_enabled = is_dark_mode_enabled;
	riyalsystem_theme.sync_layout_classes = sync_layout_classes;
	riyalsystem_theme.sync_side_menu_checkbox_effects = sync_side_menu_checkbox_effects;
})();
