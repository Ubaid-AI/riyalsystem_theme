// Copyright (c) 2021, Abdo Hamoud and contributors
// For license information, please see license.txt

function read_check(frm, fieldname) {
	if (frm.fields_dict[fieldname] && frm.fields_dict[fieldname].get_value) {
		return frm.fields_dict[fieldname].get_value();
	}
	return frm.doc[fieldname];
}

function sync_theme_settings_to_page(frm) {
	if (!frappe.riyalsystem_theme || !frappe.riyalsystem_theme.apply_theme_settings_to_page) {
		return;
	}

	const settings = {
		theme_color: frm.doc.theme_color,
		apply_on_menu: read_check(frm, 'apply_on_menu'),
		apply_on_dashboard: read_check(frm, 'apply_on_dashboard'),
		apply_on_workspace: read_check(frm, 'apply_on_workspace'),
		apply_on_navbar: read_check(frm, 'apply_on_navbar'),
		apply_dark_mode: read_check(frm, 'apply_dark_mode'),
		dark_view: read_check(frm, 'apply_dark_mode'),
		show_icon_label: read_check(frm, 'show_icon_label'),
		hide_icon_tooltip: read_check(frm, 'hide_icon_tooltip'),
	};

	frappe.theme_settings = Object.assign(frappe.theme_settings || {}, settings);
	frappe.riyalsystem_theme.apply_theme_settings_to_page(settings);
}

frappe.ui.form.on('Theme Settings', {
	refresh: function (frm) {
		$('[data-fieldname="font_family"] select').chosen({ width: '50%' });

		if (frm.doc.default_type && frm.doc.menu_opening_type !== frm.doc.default_type) {
			frm.set_value('menu_opening_type', frm.doc.default_type);
		}
	},
	apply_dark_mode: function (frm) {
		frm.set_value('dark_view', read_check(frm, 'apply_dark_mode'));
		sync_theme_settings_to_page(frm);
	},
	apply_on_navbar: sync_theme_settings_to_page,
	apply_on_menu: sync_theme_settings_to_page,
	apply_on_dashboard: sync_theme_settings_to_page,
	apply_on_workspace: sync_theme_settings_to_page,
	show_icon_label: sync_theme_settings_to_page,
	hide_icon_tooltip: sync_theme_settings_to_page,
	theme_color: sync_theme_settings_to_page,
	before_save: function (frm) {
		if (frm.doc.default_type) {
			frm.set_value('menu_opening_type', frm.doc.default_type);
		}
		frm.set_value('dark_view', read_check(frm, 'apply_dark_mode'));
	},
	after_save: function () {
		setTimeout(function () {
			frappe.ui.toolbar.clear_cache();
		}, 500);
	},
});
