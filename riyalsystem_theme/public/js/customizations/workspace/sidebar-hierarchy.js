/*
 * Hierarchical workspace sidebar (parent_page + sequence_id)
 * Collapsed mode uses the original Vue icon rail unchanged.
 */
(function () {
	'use strict';

	const EXPANDED_KEY_PREFIX = 'rst_sidebar_group_expanded_';
	const ICON_RAIL_SELECTOR = '.side-menu .side-menu-icons';
	const HOST_SELECTORS = [
		ICON_RAIL_SELECTOR,
		'.side-menu .modules-menu-list',
		'.side-mobile-menu',
	];

	let render_timer = null;
	let observer_started = false;
	let observer_guard = false;

	function cint(value) {
		return parseInt(value, 10) || 0;
	}

	function escape_html(value) {
		return frappe.utils.escape_html(String(value == null ? '' : value));
	}

	function sequence_value(page) {
		return cint(page.sequence_id);
	}

	function page_label(page) {
		return page.label || page.custom_menu_title || page.title || page.name;
	}

	function get_side_menu_vm() {
		const el = document.getElementById('side-menu-component');
		if (!el) {
			return null;
		}
		if (el.__vue_app__ && el.__vue_app__._instance && el.__vue_app__._instance.proxy) {
			return el.__vue_app__._instance.proxy;
		}
		if (el.__vue__) {
			return el.__vue__;
		}
		return null;
	}

	function is_sidebar_collapsed() {
		return document.body.classList.contains('hide-main-menu');
	}

	function build_workspace_tree(pages) {
		if (!pages || !pages.length) {
			return [];
		}

		const sorted = pages.slice().sort(function (a, b) {
			const diff = sequence_value(a) - sequence_value(b);
			if (diff !== 0) {
				return diff;
			}
			return String(page_label(a)).localeCompare(String(page_label(b)));
		});

		const nodes = {};
		sorted.forEach(function (page) {
			nodes[page.name] = Object.assign({}, page, { children: [] });
		});

		const roots = [];
		sorted.forEach(function (page) {
			const node = nodes[page.name];
			const parent_name = (page.parent_page || '').trim();
			const parent = parent_name && nodes[parent_name] ? nodes[parent_name] : null;
			if (parent && parent.name !== node.name) {
				parent.children.push(node);
			} else {
				roots.push(node);
			}
		});

		function sort_nodes(list) {
			list.sort(function (a, b) {
				const diff = sequence_value(a) - sequence_value(b);
				if (diff !== 0) {
					return diff;
				}
				return String(page_label(a)).localeCompare(String(page_label(b)));
			});
			list.forEach(function (node) {
				if (node.children && node.children.length) {
					sort_nodes(node.children);
				}
			});
		}

		sort_nodes(roots);
		return roots;
	}

	function has_active_descendant(node, active_name) {
		if (!active_name) {
			return false;
		}
		return (node.children || []).some(function (child) {
			return child.name === active_name || has_active_descendant(child, active_name);
		});
	}

	function is_group_expanded(workspace_name, default_open) {
		const key = EXPANDED_KEY_PREFIX + workspace_name;
		const stored = localStorage.getItem(key);
		if (stored === null) {
			return default_open !== false;
		}
		return stored === '1';
	}

	function set_group_expanded(workspace_name, expanded) {
		localStorage.setItem(EXPANDED_KEY_PREFIX + workspace_name, expanded ? '1' : '0');
	}

	function render_icon(page, vm) {
		const icon =
			(page.icon && page.icon.length && page.icon) ||
			(vm.module_icon && vm.module_icon[page.name]) ||
			'fal fa-folder';
		return '<i class="' + escape_html(icon) + '"></i>';
	}

	function render_tree_items(nodes, vm, options) {
		options = options || {};
		const depth = options.depth || 0;
		const active_name = vm.active_module && vm.active_module.name;

		return (nodes || [])
			.map(function (page) {
				const children = page.children || [];
				const has_children = children.length > 0;
				const child_active = has_active_descendant(page, active_name);
				const expanded = has_children
					? is_group_expanded(page.name, child_active || active_name === page.name)
					: false;
				const item_classes = ['rst-ws-item'];
				if (has_children) {
					item_classes.push('rst-ws-item--parent');
				}
				if (active_name === page.name) {
					item_classes.push('is-active');
				}
				if (child_active) {
					item_classes.push('is-parent-active');
				}
				if (expanded) {
					item_classes.push('is-expanded');
				}
				if (depth > 0) {
					item_classes.push('rst-ws-item--child');
				}

				let html =
					'<li class="' +
					item_classes.join(' ') +
					'" data-workspace="' +
					escape_html(page.name) +
					'">';
				html += '<div class="rst-ws-row">';

				if (has_children) {
					html +=
						'<button type="button" class="rst-ws-toggle" aria-expanded="' +
						(expanded ? 'true' : 'false') +
						'" aria-label="' +
						escape_html(__('Toggle {0}', [page_label(page)])) +
						'">';
					html += '<i class="far fa-angle-right rst-ws-toggle-icon"></i>';
					html += '</button>';
				} else {
					html += '<span class="rst-ws-toggle-spacer"></span>';
				}

				html +=
					'<a href="#" class="rst-ws-link' +
					(active_name === page.name ? ' active' : '') +
					'" data-workspace="' +
					escape_html(page.name) +
					'" title="' +
					escape_html(page_label(page)) +
					'">';
				html += render_icon(page, vm);
				html += '<span class="rst-ws-label">' + escape_html(page_label(page)) + '</span>';
				html += '</a>';
				html += '</div>';

				if (has_children) {
					html +=
						'<ul class="rst-ws-children' + (expanded ? ' is-visible' : '') + '">';
					html += render_tree_items(children, vm, { depth: depth + 1 });
					html += '</ul>';
				}

				html += '</li>';
				return html;
			})
			.join('');
	}

	function hide_native_workspace_list(host) {
		Array.from(host.children).forEach(function (child) {
			if (child.classList.contains('rst-workspace-tree-host')) {
				return;
			}
			child.classList.add('rst-workspace-tree-hidden');
		});
	}

	function restore_native_workspace_list(host) {
		if (!host) {
			return;
		}

		Array.from(host.children).forEach(function (child) {
			if (child.classList.contains('rst-workspace-tree-host')) {
				child.remove();
				return;
			}
			child.classList.remove('rst-workspace-tree-hidden');
		});
	}

	function restore_native_icon_rail() {
		const host = document.querySelector(ICON_RAIL_SELECTOR);
		restore_native_workspace_list(host);

		setTimeout(function () {
			const $ul = $(ICON_RAIL_SELECTOR + ' > ul');
			if (!$ul.length || typeof $.fn.niceScroll !== 'function') {
				return;
			}
			if (!$ul.getNiceScroll().length) {
				$ul.niceScroll({
					cursorcolor: 'rgba(0,0,0,0.35)',
					cursorborder: '0px',
					cursorwidth: '3px',
				});
			} else {
				$ul.getNiceScroll().resize();
			}

			if (typeof $.fn.tipsy === 'function') {
				const gravity = $('html').attr('lang') === 'ar' ? 'e' : 'w';
				$ul.find('> li > a[data-toggle="tipsy"]').tipsy({ fade: false, gravity: gravity });
			}
		}, 120);
	}

	function bind_tree_events(container, vm, is_mobile) {
		if (!container || container.dataset.rstBound === '1') {
			return;
		}
		container.dataset.rstBound = '1';

		container.addEventListener('click', function (event) {
			const toggle = event.target.closest('.rst-ws-toggle');
			if (toggle) {
				event.preventDefault();
				event.stopPropagation();
				const item = toggle.closest('.rst-ws-item--parent');
				if (!item) {
					return;
				}
				const workspace_name = item.getAttribute('data-workspace');
				const expanded = item.classList.toggle('is-expanded');
				const children_el = item.querySelector('.rst-ws-children');
				if (children_el) {
					children_el.classList.toggle('is-visible', expanded);
				}
				toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
				set_group_expanded(workspace_name, expanded);
				schedule_nicescroll(container);
				return;
			}

			const link = event.target.closest('.rst-ws-link');
			if (!link) {
				return;
			}

			event.preventDefault();
			const workspace_name = link.getAttribute('data-workspace');
			if (!workspace_name || typeof vm.open_module !== 'function') {
				return;
			}

			if (is_mobile) {
				vm.open_module(workspace_name, true);
			} else {
				$('.btn-open-modules').removeClass('active').find('i').removeClass().addClass('flaticon-menu');
				$('.modules-menu').fadeOut();
				vm.open_module(workspace_name, false);
			}
		});
	}

	function schedule_nicescroll(host) {
		if (!host) {
			return;
		}
		setTimeout(function () {
			if (typeof $.fn.niceScroll !== 'function') {
				return;
			}
			const $host = $(host);
			if (!$host.getNiceScroll().length) {
				$host.niceScroll({
					cursorcolor: 'rgba(0,0,0,0.35)',
					cursorborder: '0px',
					cursorwidth: '3px',
				});
			} else {
				$host.getNiceScroll().resize();
			}
		}, 120);
	}

	function render_tree_into(host_selector, tree_class, vm, is_mobile) {
		const host = document.querySelector(host_selector);
		if (!host || !vm.modules_list || !vm.modules_list.length) {
			return false;
		}

		let tree_host = host.querySelector('.rst-workspace-tree-host');
		if (!tree_host) {
			tree_host = document.createElement('div');
			tree_host.className = 'rst-workspace-tree-host';
			host.appendChild(tree_host);
		}

		hide_native_workspace_list(host);

		const tree = build_workspace_tree(vm.modules_list);
		tree_host.innerHTML =
			'<ul class="rst-workspace-tree list-unstyled rst-workspace-tree--expanded ' +
			(tree_class || '') +
			'">' +
			render_tree_items(tree, vm) +
			'</ul>';

		bind_tree_events(tree_host, vm, !!is_mobile);
		schedule_nicescroll(tree_host);
		return true;
	}

	function render_hierarchical_sidebar(vm) {
		vm = vm || get_side_menu_vm();
		if (!vm || !vm.modules_list || !vm.modules_list.length) {
			return;
		}

		observer_guard = true;
		try {
			if (is_sidebar_collapsed()) {
				restore_native_icon_rail();
			} else {
				render_tree_into(ICON_RAIL_SELECTOR, '', vm, false);
			}
			render_tree_into('.side-menu .modules-menu-list', 'rst-workspace-tree--popup', vm, false);
			render_tree_into('.side-mobile-menu', 'rst-workspace-tree--mobile', vm, true);
		} finally {
			observer_guard = false;
		}
	}

	function schedule_hierarchical_sidebar(vm, delays) {
		delays = delays || [0, 80, 200, 500, 900];
		if (render_timer) {
			clearTimeout(render_timer);
			render_timer = null;
		}

		let index = 0;
		function run_next() {
			if (index >= delays.length) {
				render_timer = null;
				return;
			}
			render_timer = setTimeout(function () {
				render_hierarchical_sidebar(vm || get_side_menu_vm());
				index += 1;
				run_next();
			}, delays[index]);
		}
		run_next();
	}

	function ensure_sidebar_observer() {
		if (observer_started) {
			return;
		}

		const side_menu = document.querySelector('.side-menu');
		if (!side_menu) {
			return;
		}

		const observer = new MutationObserver(function () {
			if (observer_guard) {
				return;
			}
			const vm = get_side_menu_vm();
			if (!vm || !vm.modules_list || !vm.modules_list.length) {
				return;
			}

			let needs_render = false;
			HOST_SELECTORS.forEach(function (selector) {
				const host = document.querySelector(selector);
				if (!host) {
					return;
				}

				if (is_sidebar_collapsed() && selector === ICON_RAIL_SELECTOR) {
					if (
						host.querySelector('.rst-workspace-tree-host') ||
						host.querySelector('.rst-workspace-tree-hidden')
					) {
						needs_render = true;
					}
					return;
				}

				const tree_host = host.querySelector('.rst-workspace-tree-host');
				const native_visible = Array.from(host.children).some(function (child) {
					return (
						!child.classList.contains('rst-workspace-tree-host') &&
						!child.classList.contains('rst-workspace-tree-hidden')
					);
				});
				if (!tree_host || native_visible) {
					needs_render = true;
				}
			});

			if (needs_render) {
				schedule_hierarchical_sidebar(vm, [0, 60, 180]);
			}
		});

		observer.observe(side_menu, { childList: true, subtree: true });
		observer_started = true;
	}

	function find_page_in_sidebar(vm, name) {
		if (!vm || !vm.modules_list || !name) {
			return null;
		}

		function walk(list) {
			for (let i = 0; i < list.length; i += 1) {
				const page = list[i];
				if (page.name === name) {
					return page;
				}
				if (page.children && page.children.length) {
					const found = walk(page.children);
					if (found) {
						return found;
					}
				}
			}
			return null;
		}

		return walk(build_workspace_tree(vm.modules_list));
	}

	const sidebar_api = {
		build_workspace_tree: build_workspace_tree,
		render_hierarchical_sidebar: render_hierarchical_sidebar,
		schedule_hierarchical_sidebar: schedule_hierarchical_sidebar,
		find_page_in_sidebar: find_page_in_sidebar,
		ensure_sidebar_observer: ensure_sidebar_observer,
		is_sidebar_collapsed: is_sidebar_collapsed,
		restore_native_icon_rail: restore_native_icon_rail,
	};

	frappe.provide('frappe.riyalsystem_theme.sidebar');
	Object.assign(frappe.riyalsystem_theme.sidebar, sidebar_api);

	frappe.provide('riyalsystem_theme.sidebar');
	Object.assign(riyalsystem_theme.sidebar, sidebar_api);

	$(document).ready(function () {
		ensure_sidebar_observer();
	});

	$(document).one('app-loaded', function () {
		ensure_sidebar_observer();
		schedule_hierarchical_sidebar(null, [100, 400, 900]);
	});

	$(document).one('dv-app-loaded', function () {
		schedule_hierarchical_sidebar(null, [150, 500]);
	});

	$(document).on('click', '.btn-toggle-main-menu', function () {
		setTimeout(function () {
			schedule_hierarchical_sidebar(get_side_menu_vm(), [0, 80, 250]);
		}, 60);
	});
})();
