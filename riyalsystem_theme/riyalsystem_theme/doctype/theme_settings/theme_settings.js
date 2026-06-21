// Copyright (c) 2021, Abdo Hamoud and contributors
// For license information, please see license.txt

function sync_theme_settings_to_page(frm) {
	if (!frappe.riyalsystem_theme || !frappe.riyalsystem_theme.apply_theme_settings_to_page) {
		return;
	}

	frappe.theme_settings = frappe.theme_settings || {};
	Object.assign(frappe.theme_settings, {
		theme_color: frm.doc.theme_color,
		apply_on_menu: frm.doc.apply_on_menu,
		apply_on_dashboard: frm.doc.apply_on_dashboard,
		apply_on_workspace: frm.doc.apply_on_workspace,
		apply_on_navbar: frm.doc.apply_on_navbar,
		apply_dark_mode: frm.doc.apply_dark_mode,
		dark_view: frm.doc.dark_view,
	});

	frappe.riyalsystem_theme.apply_theme_settings_to_page(frappe.theme_settings);
}

frappe.ui.form.on('Theme Settings', {
	refresh: function (frm) {
		$('[data-fieldname="font_family"] select').chosen({ width: '50%' });

		if (frm.doc.default_type && frm.doc.menu_opening_type !== frm.doc.default_type) {
			frm.set_value('menu_opening_type', frm.doc.default_type);
		}
	},
	apply_dark_mode: function (frm) {
		frm.set_value('dark_view', frm.doc.apply_dark_mode);
		sync_theme_settings_to_page(frm);
	},
	apply_on_navbar: sync_theme_settings_to_page,
	apply_on_menu: sync_theme_settings_to_page,
	apply_on_dashboard: sync_theme_settings_to_page,
	apply_on_workspace: sync_theme_settings_to_page,
	theme_color: sync_theme_settings_to_page,
	before_save: function (frm) {
		if (frm.doc.default_type) {
			frm.set_value('menu_opening_type', frm.doc.default_type);
		}
		frm.set_value('dark_view', frm.doc.apply_dark_mode);
	},
	after_save: function () {
		setTimeout(function () {
			frappe.ui.toolbar.clear_cache();
		}, 500);
	},
});
