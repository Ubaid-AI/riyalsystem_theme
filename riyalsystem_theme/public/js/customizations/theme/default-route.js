/*
 * Default landing route (Phase 3)
 * Opens Dashboard or Workspace from Theme Settings once per desk load.
 */
(function () {
	'use strict';

	let initial_route_applied = false;
	let apply_timer = null;

	function get_default_type() {
		const body = document.body;
		const settings = frappe.theme_settings || {};
		return (
			body.getAttribute('data-default-type') ||
			settings.default_type ||
			settings.menu_opening_type ||
			'Workspace'
		);
	}

	function get_default_workspace() {
		const body = document.body;
		const settings = frappe.theme_settings || {};
		return (
			body.getAttribute('data-default-workspace') ||
			settings.default_workspace ||
			''
		);
	}

	function get_default_dashboard() {
		const body = document.body;
		const settings = frappe.theme_settings || {};
		return (
			body.getAttribute('data-default-dashboard') ||
			settings.default_dashboard ||
			''
		);
	}

	function slug(value) {
		return String(value || '')
			.replace(/ /g, '-')
			.toLowerCase();
	}

	function is_generic_route(route) {
		if (!route || !route.length) {
			return true;
		}

		const first = String(route[0] || '').toLowerCase();
		if (first === 'dashboard-view') {
			return false;
		}

		if (first === 'workspaces') {
			const second = String(route[1] || '').toLowerCase();
			return !second || second === 'home' || second === 'build';
		}

		return first === 'build' || first === 'home';
	}

	function apply_default_route() {
		if (initial_route_applied || !frappe.is_app_loaded) {
			return;
		}

		const route = frappe.get_route();
		if (!is_generic_route(route)) {
			initial_route_applied = true;
			return;
		}

		const default_type = get_default_type();
		let redirected = false;

		if (default_type === 'Dashboard') {
			const dashboard_name = get_default_dashboard();
			if (dashboard_name) {
				redirected = true;
				frappe.set_route('dashboard-view', dashboard_name);
			}
		}

		if (!redirected) {
			const workspace_name = get_default_workspace();
			if (workspace_name) {
				redirected = true;
				frappe.set_route(slug(workspace_name));
			}
		}

		// Always stop after the first attempt to avoid page-change loops.
		initial_route_applied = true;
	}

	function schedule_apply_default_route() {
		if (initial_route_applied || !frappe.is_app_loaded) {
			return;
		}

		if (apply_timer) {
			clearTimeout(apply_timer);
		}

		apply_timer = setTimeout(function () {
			apply_timer = null;
			apply_default_route();
		}, 300);
	}

	$(document).one('app-loaded', schedule_apply_default_route);
})();
