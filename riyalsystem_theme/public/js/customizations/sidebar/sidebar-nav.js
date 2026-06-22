/*
 * Riyalsystem Theme - Modern single-column sidebar navigation
 * -----------------------------------------------------------
 * Builds an independent, single-column hierarchical sidebar (#rst-sidebar)
 * from the workspace list, replacing the legacy two-column .side-menu.
 *
 * Hierarchy : Workspace.parent_page  -> nesting (parent stores parent's title)
 * Order     : Workspace.sequence_id  -> handled server-side (order_by sequence_id)
 * Data      : frappe.desk.desktop.get_workspace_sidebar_items
 *             (overridden by riyalsystem_theme.desktop.get_workspace_sidebar_items)
 */

(function ($) {
	"use strict";

	const SIDEBAR_ID = "rst-sidebar";
	const SUBPANE_ID = "rst-subpane";
	const STORAGE_KEY = "rst_sidebar_collapsed";

	let SIDEBAR_PAGES = null;
	let HAS_EDIT_ACCESS = false;

	const SUBPANE_CACHE = {};
	const DOCTYPE_WS_CACHE = {};
	let CURRENT_PANE_WS = null;
	let CURRENT_SUBTAB = "menu";

	/* ---------------------------------------------------------------- utils */

	function t(text) {
		return typeof __ === "function" ? __(text) : text;
	}

	function theme_flag(name) {
		try {
			return !!parseInt((frappe.theme_settings || {})[name], 10);
		} catch (e) {
			return false;
		}
	}

	// the legacy minified Vue side-menu component is still mounted (hidden);
	// reuse its (enhanced) Edit Modules dialog instead of building a new one.
	function get_side_menu_vm() {
		const el = document.getElementById("side-menu-component");
		if (!el) return null;
		if (el.__vue_app__ && el.__vue_app__._instance && el.__vue_app__._instance.proxy) {
			return el.__vue_app__._instance.proxy;
		}
		if (el.__vue__) return el.__vue__;
		return null;
	}

	function open_edit_modules() {
		const vm = get_side_menu_vm();
		if (vm && typeof vm.open_edit_modules_dialog === "function") {
			vm.open_edit_modules_dialog();
			return;
		}
		frappe.msgprint({
			title: t("Edit Modules"),
			message: t("The menu editor is still loading. Please try again in a moment."),
			indicator: "orange",
		});
	}

	function slug(text) {
		try {
			return frappe.router.slug(text || "");
		} catch (e) {
			return (text || "").toLowerCase().replace(/\s+/g, "-");
		}
	}

	function esc(s) {
		try {
			return frappe.utils.escape_html(s);
		} catch (e) {
			return String(s == null ? "" : s).replace(/[&<>"']/g, "");
		}
	}

	// icons in this theme are stored either as FontAwesome / flaticon classes
	// (e.g. "fal fa-folder", "flaticon-businessman") OR as Frappe sprite names
	// (e.g. "education"). Detect which and render accordingly.
	function is_font_class(icon) {
		return (
			icon.indexOf("fa-") !== -1 ||
			icon.indexOf("flaticon-") !== -1 ||
			/^fa[lrsbd]?(\s|$)/.test(icon)
		);
	}

	function render_icon_markup(icon) {
		icon = (icon || "").trim();
		if (!icon) {
			icon = "fal fa-folder";
		}
		if (is_font_class(icon)) {
			return '<i class="' + esc(icon) + '"></i>';
		}
		try {
			if (frappe.utils && frappe.utils.icon) {
				return frappe.utils.icon(icon, "md");
			}
		} catch (e) {
			/* fall through */
		}
		return '<i class="fal fa-folder"></i>';
	}

	function node_icon(page) {
		// private pages use a colored indicator dot, public pages use their icon
		if (!page.public) {
			return '<span class="rst-indicator ' + (page.indicator_color || "gray") + '"></span>';
		}
		return render_icon_markup(page.icon);
	}

	function page_label(page) {
		return page.label || page.custom_menu_title || page.title || page.name || "";
	}

	function page_href(page) {
		const s = slug(page.title);
		return page.public ? "/app/" + s : "/app/private/" + s;
	}

	/* ---------------------------------------------------------- build tree */

	function build_tree(pages) {
		const nodes = pages.map(function (p) {
			return $.extend({}, p, { _children: [] });
		});

		const by_title = {};
		nodes.forEach(function (n) {
			by_title[(n.title || "").trim().toLowerCase()] = n;
		});

		const roots = [];
		nodes.forEach(function (n) {
			const parent_key = (n.parent_page || "").trim().toLowerCase();
			if (parent_key && by_title[parent_key] && by_title[parent_key] !== n) {
				by_title[parent_key]._children.push(n);
			} else {
				roots.push(n);
			}
		});

		return roots;
	}

	/* ------------------------------------------------------------- render */

	function render_item(page, depth) {
		const has_children = page._children && page._children.length;
		const $item = $('<div class="rst-nav-item"></div>')
			.attr("data-slug", slug(page.title))
			.attr("data-public", page.public ? 1 : 0)
			.attr("data-depth", depth);

		const $link = $('<a class="rst-nav-link"></a>')
			.attr("href", page_href(page))
			.css("--rst-depth", depth);

		if (!theme_flag("hide_icon_tooltip")) {
			$link.attr("title", t(page_label(page)));
		}

		$link.append('<span class="rst-nav-icon">' + node_icon(page) + "</span>");
		$link.append($('<span class="rst-nav-label"></span>').text(t(page_label(page))));

		if (has_children) {
			$item.addClass("has-children");
			$link.append(
				'<button type="button" class="rst-nav-caret" tabindex="-1" aria-label="' +
					t("Toggle submenu") +
					'"><i class="far fa-chevron-right"></i></button>'
			);
		}

		$item.append($link);

		if (has_children) {
			const $children = $('<div class="rst-nav-children"></div>');
			page._children.forEach(function (child) {
				$children.append(render_item(child, depth + 1));
			});
			$item.append($children);
		}

		return $item;
	}

	function render_nav(pages) {
		const roots = build_tree(pages);
		const $nav = $('<nav class="rst-sidebar-nav"></nav>');
		roots.forEach(function (root) {
			$nav.append(render_item(root, 0));
		});
		return $nav;
	}

	/* --------------------------------------------------------------- mount */

	function mount(pages) {
		$("#" + SIDEBAR_ID).remove();

		const $sidebar = $('<aside id="' + SIDEBAR_ID + '" class="rst-sidebar"></aside>');

		const edit_btn = HAS_EDIT_ACCESS
			? '<button type="button" class="rst-edit-menu" title="' +
				t("Edit Modules") +
				'"><i class="far fa-cog"></i></button>'
			: "";
		$sidebar.append(
			'<div class="rst-sidebar-header">' +
				'<span class="rst-sidebar-title">' +
				t("Menu") +
				"</span>" +
				edit_btn +
				"</div>"
		);

		$sidebar.append(
			'<div class="rst-sidebar-search">' +
				'<span class="rst-search-icon"><i class="far fa-search"></i></span>' +
				'<input type="text" class="rst-search-input" autocomplete="off" spellcheck="false" placeholder="' +
				t("Search menu...") +
				'">' +
				"</div>"
		);

		const $scroll = $('<div class="rst-sidebar-scroll"></div>').append(render_nav(pages));
		$sidebar.append($scroll);

		$sidebar.append(
			'<button type="button" class="rst-collapse-toggle" title="' +
				t("Collapse sidebar") +
				'">' +
				'<span class="rst-collapse-icon"><i class="far fa-chevron-double-left"></i></span>' +
				'<span class="rst-collapse-text">' +
				t("Collapse") +
				"</span>" +
				"</button>"
		);

		const $host = $(".dv-app-theme").length ? $(".dv-app-theme") : $("body");
		$host.append($sidebar);

		bind_events($sidebar);
		update_active();
		update_subpane();

		setTimeout(function () {
			$(".splash").fadeOut(200);
		}, 250);
	}

	/* -------------------------------------------------------------- events */

	function bind_events($sidebar) {
		// expand / collapse a branch (does not navigate)
		$sidebar.on("click", ".rst-nav-caret", function (e) {
			e.preventDefault();
			e.stopPropagation();
			$(this).closest(".rst-nav-item").toggleClass("open");
		});

		// navigation is handled natively by Frappe's router via the <a href>.
		// just close the mobile drawer after a pick.
		$sidebar.on("click", ".rst-nav-link", function () {
			if (window.innerWidth <= 1028) {
				$("body").removeClass("rst-mobile-open");
			}
		});

		// search filter
		$sidebar.on("input", ".rst-search-input", function () {
			filter_nav(($(this).val() || "").trim().toLowerCase());
		});

		// collapse toggle
		$sidebar.on("click", ".rst-collapse-toggle", toggle_collapse);

		// edit modules (reuses the existing dialog on the Vue component)
		$sidebar.on("click", ".rst-edit-menu", function (e) {
			e.preventDefault();
			open_edit_modules();
		});
	}

	function toggle_collapse() {
		const collapsed = $("body").toggleClass("hide-main-menu").hasClass("hide-main-menu");
		// keep the theme's navbar toggle button in sync
		$(".btn-toggle-main-menu").toggleClass("menu-shown", !collapsed);
		try {
			localStorage.setItem(STORAGE_KEY, collapsed ? "1" : "0");
		} catch (e) {
			/* ignore */
		}
	}

	/* -------------------------------------------------------------- filter */

	function filter_nav(query) {
		const $items = $("#" + SIDEBAR_ID + " .rst-nav-item");

		if (!query) {
			$items.removeClass("rst-hidden");
			return;
		}

		$items.addClass("rst-hidden");
		$items.each(function () {
			const $self = $(this);
			const label = ($self.children(".rst-nav-link").find(".rst-nav-label").text() || "").toLowerCase();
			if (label.indexOf(query) !== -1) {
				$self.removeClass("rst-hidden");
				$self.parents(".rst-nav-item").removeClass("rst-hidden").addClass("open");
				$self.find(".rst-nav-item").removeClass("rst-hidden");
			}
		});
	}

	/* -------------------------------------------------------- active state */

	function current_workspace() {
		let route;
		try {
			route = frappe.get_route();
		} catch (e) {
			return null;
		}
		if (!route || route[0] !== "Workspaces") return null;

		const is_private = route[1] === "private";
		const title = is_private ? route[2] : route[1];
		if (!title) return null;

		return { slug: slug(title), public: is_private ? 0 : 1 };
	}

	function update_active() {
		const $items = $("#" + SIDEBAR_ID + " .rst-nav-item");
		if (!$items.length) return;

		$items.removeClass("active active-trail");

		const cur = current_workspace();
		if (!cur) return;

		const $match = $items
			.filter(function () {
				return (
					$(this).attr("data-slug") === cur.slug &&
					String($(this).attr("data-public")) === String(cur.public)
				);
			})
			.first();

		if (!$match.length) return;

		$match.addClass("active");
		$match.parents(".rst-nav-item").addClass("active-trail open");

		// reveal the active item if it is scrolled out of view
		const el = $match.get(0);
		if (el && el.scrollIntoView) {
			const rect = el.getBoundingClientRect();
			if (rect.top < 80 || rect.bottom > window.innerHeight) {
				el.scrollIntoView({ block: "center" });
			}
		}
	}

	/* =====================================================================
	   SECOND PANE - current workspace's Menu (cards) + Shortcuts
	   ===================================================================== */

	function find_page_by_slug(s, is_public) {
		if (!SIDEBAR_PAGES) return null;
		for (let i = 0; i < SIDEBAR_PAGES.length; i++) {
			const p = SIDEBAR_PAGES[i];
			if (slug(p.title) === s && !!p.public === !!is_public) return p;
		}
		return null;
	}

	function find_page_by_name(name) {
		if (!SIDEBAR_PAGES || !name) return null;
		const key = String(name).toLowerCase();
		for (let i = 0; i < SIDEBAR_PAGES.length; i++) {
			const p = SIDEBAR_PAGES[i];
			if (String(p.name).toLowerCase() === key || String(p.title).toLowerCase() === key) {
				return p;
			}
		}
		return null;
	}

	// figure out which workspace's content to show in the second pane
	function resolve_active_workspace(cb) {
		let route;
		try {
			route = frappe.get_route() || [];
		} catch (e) {
			return cb(null);
		}

		if (route[0] === "Workspaces") {
			const is_private = route[1] === "private";
			const title = is_private ? route[2] : route[1];
			const page = title ? find_page_by_slug(slug(title), !is_private) : null;
			return cb(page ? { name: page.name, title: page.title, icon: page.icon } : null);
		}

		// doctype-ish context -> resolve owning workspace
		const ctx = ["List", "Form", "Tree", "report", "dashboard-view", "print", "kanban"];
		const doctype = ctx.indexOf(route[0]) !== -1 ? route[1] : null;
		if (!doctype) return cb(null);

		if (Object.prototype.hasOwnProperty.call(DOCTYPE_WS_CACHE, doctype)) {
			const cached = DOCTYPE_WS_CACHE[doctype];
			const page = cached ? find_page_by_name(cached) : null;
			return cb(page ? { name: page.name, title: page.title, icon: page.icon } : null);
		}

		frappe
			.xcall("riyalsystem_theme.api.get_doctype_parent_module", { doctype: doctype })
			.then(function (name) {
				DOCTYPE_WS_CACHE[doctype] = name || null;
				const page = name ? find_page_by_name(name) : null;
				cb(page ? { name: page.name, title: page.title, icon: page.icon } : null);
			})
			.catch(function () {
				DOCTYPE_WS_CACHE[doctype] = null;
				cb(null);
			});
	}

	function link_href(link) {
		try {
			return frappe.utils.generate_route({
				type: link.link_type || link.type || "DocType",
				name: link.link_to,
				link: link.link,
				route: link.route,
				doc_view: link.doc_view,
				is_query_report: link.is_query_report,
				report_ref_doctype: link.ref_doctype || link.report_ref_doctype,
			});
		} catch (e) {
			return "/app/" + slug(link.link_to || "");
		}
	}

	function shortcut_href(s) {
		const type = (s.type || "").toLowerCase();
		if (type === "url") return s.url || "#";
		let filters = null;
		if (s.stats_filter) {
			try {
				filters = JSON.parse(s.stats_filter);
			} catch (e) {
				filters = null;
			}
		}
		try {
			return frappe.utils.generate_route({
				type: s.type || "DocType",
				name: s.link_to,
				link: s.link,
				route: s.route,
				doc_view: filters ? "List" : s.doc_view,
				filters: filters,
				is_query_report: s.is_query_report,
				report_ref_doctype: s.ref_doctype || s.report_ref_doctype,
			});
		} catch (e) {
			return "/app/" + slug(s.link_to || "");
		}
	}

	function render_card(card) {
		const links = (card.links || []).filter(function (l) {
			return l && (l.type !== "Card Break");
		});
		if (!links.length) return null;

		const $card = $('<div class="rst-card open"></div>');
		$card.append(
			'<button type="button" class="rst-card-head">' +
				'<span class="rst-card-title"></span>' +
				'<i class="far fa-chevron-right rst-card-caret"></i>' +
				"</button>"
		);
		$card.find(".rst-card-title").text(t(card.label || ""));

		const $links = $('<div class="rst-card-links"></div>');
		links.forEach(function (link) {
			const $a = $('<a class="rst-card-link"></a>')
				.attr("href", link_href(link))
				.attr("data-name", link.link_to || "");
			$a.text(t(link.label || link.link_to || ""));
			$links.append($a);
		});
		$card.append($links);
		return $card;
	}

	function render_shortcut(s) {
		const type = (s.type || "").toLowerCase();
		const $a = $('<a class="rst-shortcut"></a>')
			.attr("href", shortcut_href(s))
			.attr("data-name", s.link_to || "");
		if (type === "url") $a.attr("target", "_blank");
		if (s.color) $a.css("--rst-shortcut-color", s.color);

		const icon = s.icon ? render_icon_markup(s.icon) : '<i class="far fa-bolt"></i>';
		$a.append('<span class="rst-shortcut-icon">' + icon + "</span>");
		$a.append($('<span class="rst-shortcut-label"></span>').text(t(s.label || s.link_to || "")));
		return $a;
	}

	function build_subpane(ws, data) {
		const cards = (data && data.cards && data.cards.items) || [];
		const shortcuts = (data && data.shortcuts && data.shortcuts.items) || [];

		const $menu = $('<div class="rst-subpane-body" data-pane="menu"></div>');
		let card_count = 0;
		cards.forEach(function (card) {
			const $c = render_card(card);
			if ($c) {
				$menu.append($c);
				card_count += 1;
			}
		});

		const $shortcuts = $('<div class="rst-subpane-body" data-pane="shortcuts"></div>');
		if (shortcuts.length) {
			const $grid = $('<div class="rst-shortcut-grid"></div>');
			shortcuts.forEach(function (s) {
				$grid.append(render_shortcut(s));
			});
			$shortcuts.append($grid);
		}

		const has_menu = card_count > 0;
		const has_shortcuts = shortcuts.length > 0;

		// nothing to show -> no pane
		if (!has_menu && !has_shortcuts) {
			hide_subpane();
			return;
		}

		$("#" + SUBPANE_ID).remove();

		const $pane = $('<aside id="' + SUBPANE_ID + '" class="rst-subpane"></aside>');

		const edit_btn = HAS_EDIT_ACCESS
			? '<button type="button" class="rst-edit-menu" title="' +
				t("Edit Modules") +
				'"><i class="far fa-cog"></i></button>'
			: "";
		const $header = $(
			'<div class="rst-subpane-header">' +
				'<span class="rst-subpane-icon">' +
				render_icon_markup(ws.icon) +
				"</span>" +
				'<span class="rst-subpane-title"></span>' +
				edit_btn +
				"</div>"
		);
		$header.find(".rst-subpane-title").text(t(ws.title));
		$pane.append($header);

		$pane.append(
			'<div class="rst-subpane-search">' +
				'<span class="rst-search-icon"><i class="far fa-search"></i></span>' +
				'<input type="text" class="rst-subpane-search-input" autocomplete="off" spellcheck="false" placeholder="' +
				t("Search...") +
				'">' +
				"</div>"
		);

		// tabs (only if both kinds exist)
		if (has_menu && has_shortcuts) {
			const $tabs = $(
				'<div class="rst-subpane-tabs">' +
					'<button type="button" class="rst-subtab" data-tab="menu"><i class="far fa-bars"></i> ' +
					t("Menu") +
					"</button>" +
					'<button type="button" class="rst-subtab" data-tab="shortcuts"><i class="far fa-star"></i> ' +
					t("Shortcuts") +
					"</button>" +
					"</div>"
			);
			$pane.append($tabs);
		}

		const active_tab = has_menu && (CURRENT_SUBTAB === "menu" || !has_shortcuts) ? "menu" : "shortcuts";

		const $scroll = $('<div class="rst-subpane-scroll"></div>');
		if (has_menu) $scroll.append($menu);
		if (has_shortcuts) $scroll.append($shortcuts);
		$pane.append($scroll);

		$("#" + SIDEBAR_ID).after($pane);

		set_subtab($pane, active_tab, has_menu, has_shortcuts);
		bind_subpane_events($pane);
		highlight_subpane_links();

		$("body").addClass("rst-subpane-open");
		CURRENT_PANE_WS = ws.name;
	}

	function set_subtab($pane, tab, has_menu, has_shortcuts) {
		if (tab === "shortcuts" && !has_shortcuts) tab = "menu";
		if (tab === "menu" && !has_menu) tab = "shortcuts";
		CURRENT_SUBTAB = tab;
		$pane.find(".rst-subtab").removeClass("active");
		$pane.find('.rst-subtab[data-tab="' + tab + '"]').addClass("active");
		$pane.find(".rst-subpane-body").attr("hidden", true);
		$pane.find('.rst-subpane-body[data-pane="' + tab + '"]').removeAttr("hidden");
	}

	function bind_subpane_events($pane) {
		$pane.on("click", ".rst-card-head", function () {
			$(this).closest(".rst-card").toggleClass("open");
		});

		$pane.on("click", ".rst-subtab", function () {
			set_subtab($pane, $(this).attr("data-tab"), true, true);
		});

		$pane.on("click", ".rst-edit-menu", function (e) {
			e.preventDefault();
			open_edit_modules();
		});

		$pane.on("click", ".rst-card-link, .rst-shortcut", function () {
			if (window.innerWidth <= 1028) $("body").removeClass("rst-mobile-open");
		});

		$pane.on("input", ".rst-subpane-search-input", function () {
			subpane_filter($pane, ($(this).val() || "").trim().toLowerCase());
		});
	}

	function subpane_filter($pane, q) {
		const $links = $pane.find(".rst-card-link, .rst-shortcut");
		if (!q) {
			$links.removeClass("rst-hidden");
			$pane.find(".rst-card").removeClass("rst-hidden");
			return;
		}
		$pane.find(".rst-card").each(function () {
			const $card = $(this);
			let visible = 0;
			$card.find(".rst-card-link").each(function () {
				const match = ($(this).text() || "").toLowerCase().indexOf(q) !== -1;
				$(this).toggleClass("rst-hidden", !match);
				if (match) visible += 1;
			});
			$card.toggleClass("rst-hidden", visible === 0).addClass("open");
		});
		$pane.find(".rst-shortcut").each(function () {
			const match = ($(this).text() || "").toLowerCase().indexOf(q) !== -1;
			$(this).toggleClass("rst-hidden", !match);
		});
	}

	function highlight_subpane_links() {
		const $pane = $("#" + SUBPANE_ID);
		if (!$pane.length) return;
		let path = "";
		try {
			path = "/app/" + (frappe.get_route() || []).join("/");
		} catch (e) {
			path = location.pathname;
		}
		$pane.find(".rst-card-link, .rst-shortcut").removeClass("active");
		$pane.find(".rst-card-link, .rst-shortcut").each(function () {
			const href = $(this).attr("href") || "";
			if (href && href !== "#" && path.indexOf(href) === 0) {
				$(this).addClass("active");
			}
		});
	}

	function hide_subpane() {
		$("#" + SUBPANE_ID).remove();
		$("body").removeClass("rst-subpane-open");
		CURRENT_PANE_WS = null;
	}

	function render_subpane(ws) {
		if (CURRENT_PANE_WS === ws.name && $("#" + SUBPANE_ID).length) {
			highlight_subpane_links();
			return;
		}
		if (SUBPANE_CACHE[ws.name]) {
			build_subpane(ws, SUBPANE_CACHE[ws.name]);
			return;
		}
		frappe
			.xcall("frappe.desk.desktop.get_desktop_page", {
				page: JSON.stringify({ name: ws.name, title: ws.title }),
			})
			.then(function (r) {
				SUBPANE_CACHE[ws.name] = r;
				build_subpane(ws, r);
			})
			.catch(function () {
				hide_subpane();
			});
	}

	function update_subpane() {
		resolve_active_workspace(function (ws) {
			if (!ws) {
				hide_subpane();
				return;
			}
			render_subpane(ws);
		});
	}

	/* ---------------------------------------------------------------- load */

	function load() {
		frappe
			.xcall("frappe.desk.desktop.get_workspace_sidebar_items")
			.then(function (r) {
				SIDEBAR_PAGES = (r && r.pages) || [];
				HAS_EDIT_ACCESS = !!(r && (r.has_access || r.has_create_access));
				mount(SIDEBAR_PAGES);
			})
			.catch(function () {
				/* keep splash logic resilient */
			});
	}

	function init() {
		if (window.__rst_sidebar_inited) return;
		window.__rst_sidebar_inited = true;

		// reflect "Side Menu" theme settings on the <body>
		$("body").toggleClass("rst-show-collapsed-labels", theme_flag("show_icon_label"));

		// restore collapsed preference before paint
		try {
			if (localStorage.getItem(STORAGE_KEY) === "1") {
				$("body").addClass("hide-main-menu");
				$(".btn-toggle-main-menu").removeClass("menu-shown");
			}
		} catch (e) {
			/* ignore */
		}

		load();

		$(document).on("page-change", function () {
			update_active();
			update_subpane();
		});

		// mobile drawer toggle reuses the theme's hamburger button
		$(document).on("click", ".dv-navbar .btn-open-mobile-menu", function () {
			$("body").toggleClass("rst-mobile-open");
		});
	}

	$(document).on("app-loaded", init);

	$(function () {
		if (window.frappe && frappe.is_app_loaded) {
			init();
		}
	});
})(jQuery);
