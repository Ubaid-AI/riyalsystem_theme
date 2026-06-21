/*
 * Workspace side-menu enhancements (Phase 2/3)
 * Patches the bundled Vue 3 Menu component without modifying the minified bundle.
 */
(function () {
	'use strict';

	const SIDEBAR_METHOD = 'frappe.desk.desktop.get_workspace_sidebar_items';
	let initial_menu_load_started = false;

	function cint(value) {
		return parseInt(value, 10) || 0;
	}

	function hide_splash() {
		$('.splash:visible').hide();
	}

	function get_menu_opening_type() {
		const body = document.body;
		const from_attr =
			body.getAttribute('data-default-type') ||
			body.getAttribute('data-menu-opening-type');
		const settings = frappe.theme_settings || {};
		return from_attr || settings.default_type || settings.menu_opening_type || 'Workspace';
	}

	function enhance_workspace_pages(pages) {
		if (!pages || !pages.length) {
			return pages || [];
		}

		return pages
			.filter(function (page) {
				return !cint(page.custom_hide_from_menu);
			})
			.map(function (page) {
				page = Object.assign({}, page);
				if (page.custom_menu_title) {
					page.label = page.custom_menu_title;
					page.title = page.custom_menu_title;
				} else if (!page.label) {
					page.label = page.title || page.name;
				}
				return page;
			});
	}

	function find_page_by_name(pages, name) {
		if (!pages || !name) {
			return null;
		}
		return pages.find(function (page) {
			return page.name === name;
		});
	}

	function get_side_menu_vm() {
		const el = document.getElementById('side-menu-component');
		if (!el) {
			return null;
		}

		if (el.__vue_app__) {
			const app = el.__vue_app__;
			if (app._instance && app._instance.proxy) {
				return app._instance.proxy;
			}
		}

		if (el.__vue__) {
			return el.__vue__;
		}

		return null;
	}

	function route_for_module(name, page) {
		if (page && cint(page.custom_open_dashboard) && page.custom_default_dashboard) {
			return '/dashboard-view/' + page.custom_default_dashboard;
		}

		if (get_menu_opening_type() === 'Dashboard') {
			const dashboard_name =
				(page && page.custom_default_dashboard) ||
				$('body').attr('data-default-dashboard') ||
				'';
			if (dashboard_name) {
				return '/dashboard-view/' + dashboard_name;
			}
		}

		return '/' + String(name).replace(/ /g, '-').toLowerCase();
	}

	function patch_frappe_call() {
		if (frappe._dv_sidebar_call_patched) {
			return;
		}

		const original_call = frappe.call.bind(frappe);

		frappe.call = function (opts) {
			// Preserve frappe.call(method, args, callback, headers) shorthand.
			if (typeof arguments[0] === 'string') {
				return original_call(
					arguments[0],
					arguments[1],
					arguments[2],
					arguments[3]
				);
			}

			opts = opts || {};

			if (opts.method === SIDEBAR_METHOD) {
				const original_callback = opts.callback;
				opts.callback = function (response) {
					if (response && response.message && response.message.pages) {
						response.message.pages = enhance_workspace_pages(response.message.pages);
						hide_splash();
					}
					if (original_callback) {
						try {
							original_callback(response);
						} catch (error) {
							console.error('[riyalsystem_theme] sidebar callback failed', error);
							hide_splash();
						}
					}
				};
			}

			return original_call(opts);
		};

		frappe._dv_sidebar_call_patched = true;
	}

	function patch_side_menu_vm() {
		const vm = get_side_menu_vm();
		if (!vm || vm._dv_menu_patched) {
			return !!vm && vm._dv_menu_patched;
		}

		if (typeof vm.get_modules === 'function') {
			vm.get_modules = function (callback) {
				frappe.call({
					type: 'POST',
					method: SIDEBAR_METHOD,
					args: {},
					callback: function (response) {
						if (response && response.message && response.message.pages) {
							response.message.pages = enhance_workspace_pages(response.message.pages);
							hide_splash();
						}

						if (typeof callback === 'function') {
							try {
								callback(response);
							} catch (error) {
								console.error('[riyalsystem_theme] sidebar callback failed', error);
								hide_splash();
							}
						}

						if (
							vm.modules_list &&
							vm.modules_list.length &&
							(!vm.active_module || !vm.active_module.name)
						) {
							const route = frappe.get_route();
							let target_name =
								route && route[0] === 'Workspaces' && route[1]
									? route[1]
									: localStorage.getItem('current_page') || vm.modules_list[0].name;
							vm.active_module =
								find_page_by_name(vm.modules_list, target_name) || vm.modules_list[0];
						}
					},
					error: function () {
						hide_splash();
					},
				});
			};
		}

		if (typeof vm.module_menu_list === 'function') {
			const original_module_menu_list = vm.module_menu_list.bind(vm);
			vm.module_menu_list = function (module_name, is_mobile) {
				const route = frappe.get_route();
				let target_name = module_name;
				if (route && route[0] === 'Workspaces' && route[1] && !is_mobile) {
					target_name = route[1];
				}

				if (vm.modules_list && vm.modules_list.length) {
					vm.active_module = find_page_by_name(vm.modules_list, target_name);
					if (!vm.active_module) {
						vm.active_module = vm.modules_list.find(function (page) {
							return page.title === target_name || page.label === target_name;
						});
					}

					if (vm.active_module && vm.active_module.name) {
						hide_splash();
						if (
							vm.module_items_list[vm.active_module.name] &&
							vm.module_items_list[vm.active_module.name].length
						) {
							vm.after_side_menu_items();
						} else if (typeof vm.get_module_items === 'function') {
							vm.get_module_items(vm.active_module.name, function (response) {
								if (
									response &&
									response.message &&
									response.message.cards &&
									response.message.cards.items
								) {
									vm.module_items_list[vm.active_module.name] =
										response.message.cards.items;
								}
								if (
									response &&
									response.message &&
									response.message.shortcuts &&
									response.message.shortcuts.items
								) {
									vm.module_shortcuts_list[vm.active_module.name] =
										response.message.shortcuts.items;
								}
								vm.after_side_menu_items();
							});
						}
						vm.after_side_menu();
						return;
					}
				}

				return original_module_menu_list(module_name, is_mobile);
			};
		}

		if (typeof vm.open_module === 'function') {
			vm.open_module = function (name, is_mobile) {
				const page = find_page_by_name(vm.modules_list, name);
				const route = route_for_module(name, page);

				$('.btn-open-modules').removeClass('active').find('i').removeClass().addClass('flaticon-menu');
				$('.modules-menu').fadeOut();
				vm.menu_search = '';

				setTimeout(function () {
					vm.module_menu_list(name, is_mobile);
				}, 100);

				if (!is_mobile) {
					frappe.set_route(route);
					$('.btn-toggle-main-menu').addClass('menu-shown');
					$('body').removeClass('hide-main-menu');
				} else if (vm.theme_settings && cint(vm.theme_settings.open_workspace_on_mobile_menu)) {
					frappe.set_route(route);
					vm.is_shown_mobile_menu = false;
				} else {
					vm.is_shown_mobile_menu = true;
				}
			};
		}

		vm._dv_menu_patched = true;
		return true;
	}

	function trigger_initial_menu_load() {
		if (initial_menu_load_started || !$('.splash:visible').length) {
			return;
		}

		const vm = get_side_menu_vm();
		if (!vm || typeof vm.get_theme_settings !== 'function') {
			return;
		}

		initial_menu_load_started = true;

		vm.get_theme_settings(function () {
			if (typeof vm.get_module_name_from_doctype === 'function') {
				vm.get_module_name_from_doctype();
			} else if (typeof vm.module_menu_list === 'function') {
				vm.module_menu_list('Home');
			}
		});
	}

	function ensure_side_menu_patch() {
		patch_frappe_call();

		if (patch_side_menu_vm()) {
			trigger_initial_menu_load();
			return;
		}

		if (frappe._dv_side_menu_patch_timer) {
			return;
		}

		let attempts = 0;
		frappe._dv_side_menu_patch_timer = setInterval(function () {
			attempts += 1;
			if (patch_side_menu_vm()) {
				clearInterval(frappe._dv_side_menu_patch_timer);
				frappe._dv_side_menu_patch_timer = null;
				trigger_initial_menu_load();
			} else if (attempts > 50) {
				clearInterval(frappe._dv_side_menu_patch_timer);
				frappe._dv_side_menu_patch_timer = null;
				hide_splash();
			}
		}, 200);
	}

	function on_app_ready() {
		ensure_side_menu_patch();
		setTimeout(trigger_initial_menu_load, 100);
		setTimeout(function () {
			if ($('.splash:visible').length) {
				hide_splash();
			}
		}, 8000);
	}

	$(document).one('app-loaded', on_app_ready);
	$(document).one('dv-app-loaded', function () {
		setTimeout(trigger_initial_menu_load, 150);
	});
	$(document).ready(function () {
		if (document.getElementById('side-menu-component')) {
			ensure_side_menu_patch();
		}
	});
})();
