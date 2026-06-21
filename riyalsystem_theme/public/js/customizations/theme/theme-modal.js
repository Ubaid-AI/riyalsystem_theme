/*
 * Navbar quick theme settings modal
 */
(function () {
	'use strict';

	const THEME_COLORS = [
		'Blue',
		'Green',
		'Red',
		'Orange',
		'Yellow',
		'Pink',
		'Violet',
		'Dark Gray',
	];

	function as_theme_check(value) {
		return frappe.riyalsystem_theme && frappe.riyalsystem_theme.as_theme_check
			? frappe.riyalsystem_theme.as_theme_check(value)
			: parseInt(value, 10) ? 1 : 0;
	}

	function get_settings() {
		return frappe.riyalsystem_theme && frappe.riyalsystem_theme.normalize_theme_settings
			? frappe.riyalsystem_theme.normalize_theme_settings(frappe.theme_settings || {})
			: frappe.theme_settings || {};
	}

	function get_active_color() {
		const settings = get_settings();
		return (
			$('body').attr('data-theme-colorname') ||
			settings.theme_color ||
			'Blue'
		);
	}

	function color_class_name(color) {
		return 'dv-' + String(color).replace(/ /g, '-') + '-style';
	}

	function apply_settings_to_page(values, theme_color) {
		const settings = Object.assign({}, get_settings(), values, {
			theme_color: theme_color,
			apply_on_menu: as_theme_check(values.apply_on_menu),
			apply_on_dashboard: as_theme_check(values.apply_on_dashboard),
			apply_on_workspace: as_theme_check(values.apply_on_workspace),
			apply_on_navbar: as_theme_check(values.apply_on_navbar),
			apply_dark_mode: as_theme_check(values.apply_dark_mode),
			dark_view: as_theme_check(values.apply_dark_mode),
		});

		if (frappe.riyalsystem_theme && frappe.riyalsystem_theme.apply_theme_settings_to_page) {
			frappe.riyalsystem_theme.apply_theme_settings_to_page(settings);
		}
	}

	function remove_legacy_theme_handlers() {
		$(document).off('click', '.open-theme-setting');
		$(document).off('click', '.open-theme-setting-legacy-disabled');
		$(document).off('click', '.theme-setting-colors-select.theme-setting-modal button');
	}

	function build_color_picker_html() {
		const active_color = get_active_color();

		return `
			<div class="theme-setting-colors-select theme-setting-modal" style="margin-bottom: 5px;">
				<h4>${__('Theme Colors')}</h4>
				<div class="dv-row dv-row-sm">
					${THEME_COLORS.map(function (color) {
						const is_active = active_color === color ? 'active' : '';
						return `<div class="dv-col">
							<button type="button" class="${is_active}" data-color="${color}" data-class="${color_class_name(color)}">${__(color)}</button>
						</div>`;
					}).join('')}
				</div>
			</div>
		`;
	}

	function bind_color_picker(dialog) {
		dialog.$wrapper
			.off('click.dv-theme-colors', '.theme-setting-colors-select.theme-setting-modal button')
			.on('click.dv-theme-colors', '.theme-setting-colors-select.theme-setting-modal button', function (event) {
				event.preventDefault();
				dialog.$wrapper.find('.theme-setting-colors-select.theme-setting-modal button').removeClass('active');
				$(this).addClass('active');
			});
	}

	function open_theme_settings_dialog() {
		const settings = get_settings();
		const dialog = new frappe.ui.Dialog({
			title: __('Theme Settings'),
			fields: [
				{
					label: __('Colors'),
					fieldname: 'colors_icons',
					fieldtype: 'HTML',
					options: build_color_picker_html(),
				},
				{
					fieldname: 'apply_color_and_background_section',
					fieldtype: 'Section Break',
					label: __('Apply Color and Background'),
				},
				{
					fieldname: 'html_space_before',
					label: '',
					fieldtype: 'HTML',
					options: '<div style="height:10px;"></div>',
				},
				{
					fieldname: 'apply_on_menu',
					label: __('Apply on Menu'),
					fieldtype: 'Check',
					default: as_theme_check(settings.apply_on_menu),
				},
				{
					fieldname: 'apply_on_dashboard',
					label: __('Apply on Dashboard'),
					fieldtype: 'Check',
					default: as_theme_check(settings.apply_on_dashboard),
				},
				{
					fieldname: 'apply_on_workspace',
					label: __('Apply on Workspace'),
					fieldtype: 'Check',
					default: as_theme_check(settings.apply_on_workspace),
				},
				{
					fieldname: 'apply_on_navbar',
					label: __('Apply on Navbar'),
					fieldtype: 'Check',
					default: as_theme_check(settings.apply_on_navbar),
				},
				{
					fieldname: 'apply_dark_mode',
					label: __('Apply Dark Mode'),
					fieldtype: 'Check',
					default: as_theme_check(settings.apply_dark_mode || settings.dark_view),
				},
			],
			primary_action_label: __('Save Settings'),
			primary_action: function () {
				const values = dialog.get_values();
				if (!values) {
					return;
				}

				const $active = dialog.$wrapper.find(
					'.theme-setting-colors-select.theme-setting-modal button.active'
				);
				const theme_color = $active.data('color') || get_active_color();
				const payload = {
					theme_color: theme_color,
					apply_on_menu: as_theme_check(values.apply_on_menu),
					apply_on_dashboard: as_theme_check(values.apply_on_dashboard),
					apply_on_workspace: as_theme_check(values.apply_on_workspace),
					apply_on_navbar: as_theme_check(values.apply_on_navbar),
					apply_dark_mode: as_theme_check(values.apply_dark_mode),
				};

				frappe.call({
					method: 'riyalsystem_theme.api.update_theme_settings',
					args: payload,
					callback: function () {
						frappe.theme_settings = Object.assign(frappe.theme_settings || {}, payload, {
							dark_view: payload.apply_dark_mode,
						});
						apply_settings_to_page(payload, theme_color);
						frappe.ui.toolbar.clear_cache();
						setTimeout(function () {
							dialog.hide();
						}, 300);
					},
				});
			},
		});

		bind_color_picker(dialog);
		dialog.show();
	}

	function on_theme_button_click(event) {
		const target = event.target.closest('.open-theme-setting');
		if (!target) {
			return;
		}
		event.preventDefault();
		event.stopPropagation();
		event.stopImmediatePropagation();
		open_theme_settings_dialog();
		return false;
	}

	function bind_theme_modal() {
		remove_legacy_theme_handlers();
		document.removeEventListener('click', on_theme_button_click, true);
		document.addEventListener('click', on_theme_button_click, true);
	}

	remove_legacy_theme_handlers();
	$(document).ready(bind_theme_modal);
	$(document).one('app-loaded', bind_theme_modal);
})();
