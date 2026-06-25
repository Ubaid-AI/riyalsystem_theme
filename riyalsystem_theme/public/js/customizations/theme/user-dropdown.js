/*
 * User logout dropdown styling hooks (icons via CSS)
 * + adds an "About Us" entry just before "Log out".
 */
(function () {
	'use strict';

	const ABOUT_URL = 'https://riyalsystem.com.sa/';

	function label(text) {
		return typeof window.__ === 'function' ? window.__(text) : text;
	}

	function add_about_us($menu) {
		if ($menu.find('.dv-about-us').length) {
			return;
		}

		const $about = $(
			'<a class="dropdown-item dv-about-us" target="_blank" rel="noopener noreferrer"></a>'
		)
			.attr('href', ABOUT_URL)
			.text(label('About Us'));

		const $logout = $menu
			.find('.dropdown-item')
			.filter(function () {
				const onclick = ($(this).attr('onclick') || '').toLowerCase();
				const text = ($(this).text() || '').trim().toLowerCase();
				return (
					onclick.indexOf('logout') > -1 ||
					text === 'log out' ||
					text === 'logout' ||
					text === 'sign out'
				);
			})
			.first();

		if ($logout.length) {
			$logout.before($about);
		} else {
			$menu.append($about);
		}
	}

	function enhance_user_dropdown() {
		const $menu = $('.dv-navbar .dropdown-user .dropdown-menu.dropdown-menu-right').first();
		if (!$menu.length) {
			return false;
		}

		if ($menu.attr('id') !== 'navbar-user-dropdown-menu') {
			$menu.attr('id', 'navbar-user-dropdown-menu');
		}

		add_about_us($menu);
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
