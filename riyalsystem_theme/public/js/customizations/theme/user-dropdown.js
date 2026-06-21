/*
 * User logout dropdown styling hooks (icons via CSS)
 */
(function () {
	'use strict';

	function enhance_user_dropdown() {
		const $menu = $('.dv-navbar .dropdown-user .dropdown-menu.dropdown-menu-right').first();
		if (!$menu.length || $menu.attr('id') === 'navbar-user-dropdown-menu') {
			return !!$menu.length;
		}

		$menu.attr('id', 'navbar-user-dropdown-menu');
		return true;
	}

	function ensure_user_dropdown() {
		if (enhance_user_dropdown()) {
			return;
		}

		if (frappe._dv_user_dropdown_patch_timer) {
			return;
		}

		let attempts = 0;
		frappe._dv_user_dropdown_patch_timer = setInterval(function () {
			attempts += 1;
			if (enhance_user_dropdown() || attempts > 50) {
				clearInterval(frappe._dv_user_dropdown_patch_timer);
				frappe._dv_user_dropdown_patch_timer = null;
			}
		}, 200);
	}

	$(document).one('app-loaded', ensure_user_dropdown);
	$(document).ready(ensure_user_dropdown);
})();
