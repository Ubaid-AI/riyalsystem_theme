/*
 * Theme Settings helpers (Phase 3)
 * Keeps legacy body/jQuery data in sync with Theme Settings fields.
 */
(function () {
	'use strict';

	function get_opening_type() {
		const body = document.body;
		const settings = frappe.theme_settings || {};
		return (
			body.getAttribute('data-default-type') ||
			body.getAttribute('data-menu-opening-type') ||
			settings.default_type ||
			settings.menu_opening_type ||
			'Workspace'
		);
	}

	function sync_menu_opening_data() {
		const opening_type = get_opening_type();
		const $body = $('body');

		$body.attr('data-default-type', opening_type);
		$body.attr('data-menu-opening-type', opening_type);
		$body.data('default-type', opening_type);
		$body.data('defaultType', opening_type);
		$body.data('menu-opening-type', opening_type);
		$body.data('menuOpeningType', opening_type);
	}

	$(document).ready(sync_menu_opening_data);
	$(document).one('app-loaded', sync_menu_opening_data);
})();
