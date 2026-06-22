# AGENTS.md — Riyalsystem Theme Developer & AI Onboarding Guide

> Read this file FIRST before changing anything in this app.
> It is written for both human developers and AI agents picking up a new task
> with zero prior context. It explains what the app is, how it is wired, how to
> build/deploy, the conventions to follow, and the safe recipes for the most
> common kinds of work.

---

## 1. What this app is

`riyalsystem_theme` is a **Frappe 15 / ERPNext desk theme app**. It restyles and
extends the ERPNext "desk" (the logged-in admin UI at `/app`) — navbar, sidebar,
workspaces, login page, colors, dark mode, fonts, and layout.

- **App name (module):** `riyalsystem_theme`
- **Publisher:** Abdo Hamoud
- **License:** MIT
- **Installed on site:** `site1.local`
- **Product display name in UI:** "Salasah ERP" (see `www/app.html` `<title>` and splash)

### Relationship to `datavalue_theme_15`

There are **two theme apps** in this bench:

| App | Role |
| --- | --- |
| `datavalue_theme_15` | The **original** theme app (baseline / upstream). Do NOT edit for new features. |
| `riyalsystem_theme`  | The **enhancement fork** where ALL new work happens. This is the active app. |

Many file names still carry the legacy `datavalue_theme` prefix (e.g.
`datavalue_theme.bundle.scss`, `datavalue_theme.app.min.js`) because this app was
forked from `datavalue_theme_15`. That naming is intentional — keep it.

**Rule of thumb:** implement every new feature/fix in `riyalsystem_theme`.

---

## 2. How a desk page boots (request flow)

The desk is served by a custom web page, NOT the stock Frappe `/app` template.

```
Browser → /app  →  www/app.py (get_context)  →  www/app.html (Jinja)
                       │                              │
                       │ injects theme_settings,      │ renders <html>/<body> with
                       │ theme_color, dark_theme,      │ theme classes + data-* attrs,
                       │ build_version, boot, etc.     │ then loads JS/CSS includes
                       ▼                              ▼
             Theme Settings (Single doctype)   datavalue_theme.app.min.js (core desk, Vue)
                                                + datavalue_theme.bundle.css (compiled SCSS)
                                                + js/customizations/**/*.js (our feature scripts)
```

Key consequences:
- The `<html>`/`<body>` tag classes and `data-*` attributes are set **server-side**
  in `www/app.html` from Theme Settings (e.g. `dv-dark-style`, `layout-menu-color-style`,
  `data-theme="dark"`). Client JS (`dark-mode.js`) re-syncs them at runtime.
- `frappe.theme_settings` is available in JS as a global object (injected in `app.html`).
- `--primary`, `--blue-*`, etc. CSS variables are **remapped** in the inline `<style>`
  block of `app.html` based on the selected `theme_color`. This is why our SCSS can use
  `var(--blue-500)` and automatically get the user's chosen theme color.

---

## 3. Directory map (source files that matter)

```
riyalsystem_theme/
├── AGENTS.md                         ← you are here
├── README.md
├── pyproject.toml
└── riyalsystem_theme/
    ├── hooks.py                      ← app hooks: asset includes, whitelisted overrides, fixtures, after_migrate
    ├── api.py                        ← whitelisted Python endpoints (theme settings, workspace menu editing, events)
    ├── desktop.py                    ← override of get_workspace_sidebar_items (sidebar data source)
    ├── modules.txt / patches.txt
    │
    ├── www/
    │   ├── app.py                    ← desk page controller: builds Jinja context from Theme Settings
    │   ├── app.html                  ← desk HTML shell: body classes, CSS vars, <script> includes
    │   ├── login.py / login.html     ← custom login page
    │
    ├── templates/
    │   ├── side-menu.html            ← legacy Vue side-menu mount point (#side-menu-component) — STILL USED for Edit Modules dialog
    │   └── sidemenu.html
    │
    ├── public/
    │   ├── js/
    │   │   ├── datavalue_theme.app.min.js   ← MINIFIED core desk bundle (Vue). Do NOT hand-edit.
    │   │   ├── datavalue_theme.web.min.js   ← minified website bundle
    │   │   ├── datavalue_theme.js           ← desk bootstrap (sets data-theme, etc.)
    │   │   └── customizations/              ← OUR editable feature scripts (loaded individually in app.html)
    │   │       ├── sidebar/sidebar-nav.js   ← ★ the custom modern sidebar + second pane (main UI feature)
    │   │       ├── theme/dark-mode.js       ← applies Theme Settings (dark mode, color classes, side-menu flags)
    │   │       ├── theme/settings.js        ← theme settings application helpers
    │   │       ├── theme/theme-bools.js     ← boolean/normalization helpers (frappe.riyalsystem_theme.*)
    │   │       ├── theme/theme-modal.js     ← theme settings modal
    │   │       ├── theme/user-dropdown.js
    │   │       ├── theme/default-route.js   ← default workspace/dashboard routing
    │   │       ├── workspace/edit-modules.js← "Edit Modules" Vue dialog logic (sequence/title/icon/parent/hide)
    │   │       ├── erpnext/document-flow.js
    │   │       └── file/file.js
    │   │
    │   └── scss/
    │       ├── datavalue_theme.bundle.scss  ← ★ the bundle entrypoint: @imports all partials (ORDER MATTERS)
    │       ├── datavalue_theme.scss
    │       ├── dv-login.scss
    │       └── partials/
    │           ├── _sidebar-nav.scss        ← ★ styles for the custom sidebar + second pane (rst-* classes)
    │           ├── _dark-style.scss         ← dark mode variable remaps (body.dv-dark-style, html[data-theme="dark"])
    │           ├── _layouts-color.scss      ← themed-color layout classes
    │           ├── _side-menu.scss          ← legacy side menu styles
    │           ├── _header.scss _body.scss _content.scss _layout.scss _responsive.scss _rtl.scss ...
    │           └── _<color>-style.scss       ← per-color palettes (green/red/orange/yellow/violet/pink/dark-gray)
    │
    └── riyalsystem_theme/                   ← the doctype module folder
        ├── doctype/theme_settings/          ← ★ Theme Settings (Single) — all user-facing theme toggles
        ├── doctype/slideshow_photos/
        └── custom/workspace.json            ← custom fields added to Workspace (custom_menu_title, custom_hide_from_menu, etc.)
```

Generated/compiled output (do NOT edit by hand, regenerated by `bench build`):
- `public/dist/css/datavalue_theme.bundle.<HASH>.css`
- `sites/assets/riyalsystem_theme/dist/css/datavalue_theme.bundle.<HASH>.css` (served copy)
- `.sass-cache/` folders.

---

## 4. The custom sidebar (the flagship feature)

This is the most-developed area. Understand it before touching navigation.

### 4.1 Files
- **Logic:** `public/js/customizations/sidebar/sidebar-nav.js`
- **Styles:** `public/scss/partials/_sidebar-nav.scss`
- **Data source:** `desktop.py::get_workspace_sidebar_items` (overrides Frappe core via `hooks.py`)

### 4.2 What it renders
A from-scratch, single-column, modern sidebar that **replaces** the legacy
two-column Vue side menu. It has two parts:

1. **Main tree** (`#rst-sidebar`, `.rst-*` classes): hierarchical workspace list.
   - Hierarchy is built from the **Workspace** doctype: `parent_page` → parent/child,
     `sequence_id` → order.
   - Header with title + an "Edit Modules" gear button (only if user has edit access).
   - Search box, collapse toggle (collapsed mode = icons only with hover-peek).
2. **Second pane** (`#rst-subpane`): when a workspace is open, a VS-Code/Outlook-style
   second column slides in showing that workspace's **Menu (cards/links)** and
   **Shortcuts** in tabs, with its own search.

### 4.3 The legacy Vue side menu is HIDDEN, not removed
- `templates/side-menu.html` still mounts `#side-menu-component` (a Vue app from the
  minified core bundle). Our SCSS sets it to `width:0 !important; display:none`.
- **Why keep it:** the "Edit Modules" dialog (end-user editor for sequence, title,
  icon, parent page, hide-from-menu) lives in that Vue component. Our gear button calls
  it via `get_side_menu_vm()` → `open_edit_modules_dialog()`. **Do not delete the legacy
  mount** or the editor breaks. We intentionally reuse it instead of rebuilding it.

### 4.4 Key JS internals (sidebar-nav.js)
IIFE module. Important symbols:
- `SIDEBAR_ID = "rst-sidebar"`, `SUBPANE_ID = "rst-subpane"`, `STORAGE_KEY` (collapse persistence)
- `theme_flag(name)` — reads booleans from `frappe.theme_settings` (e.g. `show_icon_label`, `hide_icon_tooltip`).
- `is_font_class()` / `render_icon_markup()` — icons are a **mix** of FontAwesome/flaticon
  classes (e.g. `far fa-cog`) and Frappe SVG sprite names. This detects which and renders
  `<i>` vs `frappe.utils.icon()`. If icons disappear, look here.
- `build_tree(pages)` — turns flat pages into parent/child tree via `parent_page`.
- `render_nav` / `render_item` — builds the main list markup.
- `mount(pages)` — (re)builds the whole sidebar DOM.
- `update_active()` / `current_workspace()` — active-state highlighting from the route.
- `resolve_active_workspace()` — figures out which workspace the second pane should show,
  including resolving a doctype's parent module (cached in `DOCTYPE_WS_CACHE` via
  `riyalsystem_theme.api.get_doctype_parent_module`).
- `build_subpane` / `set_subtab` / `render_subpane` / `update_subpane` — second-pane lifecycle.
- `SUBPANE_CACHE` — caches per-workspace desktop page data.

### 4.5 Body classes the sidebar relies on
- `hide-main-menu` → collapsed mode (icons only).
- `rst-show-collapsed-labels` → show labels under icons in collapsed mode (`show_icon_label`).
- `rst-subpane-open` → second pane visible (adds left margin to content).
- `rst-mobile-open` → mobile drawer open.
- `layout-menu-color-style` / `layout-navbar-color-style` → themed color applied (see §6).
- `dv-dark-style` / `html[data-theme="dark"]` → dark mode (see §7).

---

## 5. Backend: overrides & whitelisted API

### 5.1 Whitelisted method override (`hooks.py`)
```python
override_whitelisted_methods = {
    "frappe.desk.desktop.get_workspace_sidebar_items":
        "riyalsystem_theme.desktop.get_workspace_sidebar_items",
}
```
`desktop.py::get_workspace_sidebar_items` returns `{pages, has_access, has_create_access}`.
It includes the theme's custom Workspace fields, honors `custom_hide_from_menu`,
applies `custom_menu_title` as label, and grants full visibility to the
**"Workspace Manager"** role.

### 5.2 Whitelisted endpoints (`api.py`) — callable from JS via `frappe.xcall("riyalsystem_theme.api.<fn>")`
- `get_theme_settings()` — read all Theme Settings (guest-allowed).
- `update_theme_settings(**data)` — write color/apply flags/dark mode.
- `get_doctype_parent_module(doctype)` — resolve a doctype to its owning Workspace (used by second pane).
- `update_menu_modules(modules)` — bulk create/update/delete Workspaces from the Edit Modules dialog
  (title, icon, `sequence_id`, `parent_page`, `custom_hide_from_menu`, dashboards).
- `update_workspace_order(workspaces)` / `update_workspace_order_with_parent(...)` — reorder + reparent.
- `update_workspace_data(name, custom_title, icon)`.
- `get_module_name_from_doctype(...)`, `change_language(...)`, `get_current_language()`,
  `get_company_logo()`, `get_events(...)`.

### 5.3 `after_migrate` + fixtures
- `after_migrate = ["riyalsystem_theme.workspace_process_flows.sync.sync_blocks"]` —
  rebuilds the "Process Flow" Custom HTML Blocks after each migrate.
- `fixtures` exports the `RST * Process Flow` Custom HTML Block records.

---

## 6. Theme Settings (the config surface)

`Theme Settings` is a **Single doctype** (`doctype/theme_settings/`). Its values drive
everything. Read in JS via `frappe.theme_settings`, in Python via `www/app.py`.

Most relevant fields by tab:
- **General/Color:** `theme_color` (Select), `dark_view`, `apply_dark_mode`.
- **Side Menu:** `show_icon_label` ("Show Labels in Collapsed Mode"),
  `hide_icon_tooltip` ("Hide Tooltips in Collapsed Mode").
- **Theme Layout:** `always_close_sub_menu`, `menu_opening_type`, `hide_language_icon`,
  `show_help_icon`, `font_family`, `open_workspace_on_mobile_menu`.
- **Layout:** `apply_on_menu`, `apply_on_navbar`, `apply_on_dashboard`, `apply_on_workspace`.
- **Defaults:** `default_type` ("Default Open"), `default_workspace`, `default_dashboard`.
- Login page: `background_type`, `background_photo`, `slideshow`, `full_page_background`, `favicon`, `loading_image`, `theme_logo`.

How settings reach the UI:
- `www/app.py` reads them from `tabSingles` and exposes as Jinja context.
- `www/app.html` turns flags into body classes (e.g. `apply_on_menu` →
  `layout-menu-color-style`) and remaps `--primary`/`--blue-*` CSS vars to `theme_color`.
- `customizations/theme/dark-mode.js` re-applies the same classes at runtime
  (function `apply_theme_settings_to_page`) so changes take effect without a hard reload.

---

## 7. Dark mode & themed color — how the CSS layering works

This bit has bitten us before; understand the cascade order.

### Dark mode triggers (any of these means "dark"):
- `body.dv-dark-style`, `body.dv-theme-dark`
- `html[data-theme="dark"]`, `html[data-theme-mode="dark"]`

Dark mode remaps core CSS variables in `_dark-style.scss`:
```scss
body.dv-dark-style, html[data-theme="dark"] {
  --fg-color: #242a30;
  --border-color: #161b21;
  --text-color: var(--gray-400);
  ...
}
```
So any element using `var(--fg-color)` auto-darkens.

### Themed color triggers:
- `body.layout-menu-color-style` (from `apply_on_menu`)
- `body.layout-navbar-color-style` (from `apply_on_navbar`)
These paint surfaces with light `--blue-*` tints (remapped to the chosen color).

### The conflict & the fix (important!)
The themed-color rules and the dark rules can both target `.rst-sidebar`/`.rst-subpane`.
With equal specificity, **CSS source order wins**. The themed-color block appears later
in `_sidebar-nav.scss`, so in dark mode it would override dark and keep the sidebar light.

**Resolution (already implemented):** there is an **authoritative dark block at the very
end of `_sidebar-nav.scss`** using `!important` and matching all four dark triggers. It is
placed last on purpose so dark always wins over the themed-color tints.

> When you add new `.rst-*` elements: if they have a themed-color variant, also add a dark
> override in that final authoritative block, or they will stay light in dark mode when
> `apply_on_menu`/`apply_on_navbar` is enabled.

---

## 8. Build & deploy workflow (CRITICAL)

SCSS and bundled JS are **compiled**. Editing source files alone changes nothing in the
browser until you rebuild. CSS bundles are content-hashed (e.g.
`datavalue_theme.bundle.2LXVI6XZ.css`), so the served filename changes on each build —
`bench build` updates the references for you.

### After editing SCSS or bundled assets:
```bash
cd /home/frappe/frappe-bench
bench build --app riyalsystem_theme
bench --site site1.local clear-cache
```

### After editing `customizations/**/*.js`:
These are included individually (not bundled) with `?ver={{ build_version }}` cache-busting.
A `bench build` bumps the build version; a hard browser refresh (Ctrl/Cmd+Shift+R) is
usually enough. When in doubt, run the two commands above.

### After editing Python (`*.py`, hooks, doctypes):
```bash
bench --site site1.local migrate     # if doctype/schema/fixtures changed
bench --site site1.local clear-cache
# restart if a long-running process caches code:
bench restart      # or: bench --site site1.local console to test
```

### Verifying a CSS change actually compiled
Grep the **served** bundle (path printed by `bench build`):
```
sites/assets/riyalsystem_theme/dist/css/datavalue_theme.bundle.<HASH>.css
```
(Use Glob to find the current hash; it changes each build.)

---

## 9. Conventions & house rules

- **All new desk features go in `riyalsystem_theme`**, never `datavalue_theme_15`.
- **CSS class prefix `rst-`** for everything we add to the sidebar/panes. Keep it.
- **Never hand-edit** `*.min.js`, `dist/`, or `.sass-cache/` files.
- **SCSS import order matters** — register new partials in
  `public/scss/datavalue_theme.bundle.scss`. `_sidebar-nav.scss` is imported LAST so its
  overrides win; the authoritative dark block must remain at the end of that file.
- **Reuse, don't rebuild** existing working pieces (e.g. the Edit Modules Vue dialog).
- **Icons are mixed** (FontAwesome class strings vs Frappe sprite names) — route new icon
  rendering through the existing helpers in `sidebar-nav.js`.
- **RTL:** the desk runs in both LTR and RTL (`dir` set in `app.html`). Prefer CSS logical
  properties (`inset-inline-start`, `margin-inline-start`, `border-inline-end`) over
  left/right so RTL keeps working. There is also `_rtl.scss`.
- **Theme color:** use `var(--primary)` and `var(--blue-50..900)` instead of hardcoded hex
  so the user's chosen `theme_color` flows through automatically.
- **Don't add narrating code comments.** Comment only non-obvious intent.

---

## 10. Common task recipes

### A. Add a new toggle to Theme Settings that affects the sidebar
1. Add the field in `doctype/theme_settings/theme_settings.json` (+ `bench --site site1.local migrate`).
2. Expose it if needed in `www/app.py` context and/or `api.py::get_theme_settings`.
3. Read it in JS via `frappe.theme_settings.<field>` (use `theme_flag()` for booleans).
4. If it sets a body class, also set it server-side in `www/app.html` and at runtime in
   `customizations/theme/dark-mode.js` (`apply_theme_settings_to_page`).
5. Add the matching SCSS in `_sidebar-nav.scss` (and a dark variant in the final block).
6. `bench build --app riyalsystem_theme && bench --site site1.local clear-cache`.

### B. Change sidebar appearance/behavior
- Markup/logic → `sidebar-nav.js`; styles → `_sidebar-nav.scss`. Rebuild CSS. Remember the
  dark + themed-color cascade rules in §7.

### C. Change what data appears in the sidebar
- Edit `desktop.py::get_workspace_sidebar_items` (server filtering / fields).
- Menu hierarchy/order is Workspace `parent_page` / `sequence_id` — editable by end users
  via the Edit Modules gear (which calls `api.py::update_menu_modules`).

### D. Add a new customization script
1. Create `public/js/customizations/<area>/<name>.js` (wrap in an IIFE).
2. Add a `<script src=".../<area>/<name>.js?ver={{ build_version }}">` line in `www/app.html`
   (order matters; it loads after the core bundle).
3. `bench build --app riyalsystem_theme && bench --site site1.local clear-cache`.

### E. Add/modify a color palette
- Edit/add `partials/_<color>-style.scss`, import it in the bundle, rebuild. The selected
  palette is chosen via Theme Settings `theme_color` and remapped to `--blue-*` in `app.html`.

---

## 11. Gotchas / things that have broken before

- **"Wide ugly" collapsed sidebar:** caused by the legacy Vue two-column menu fighting our
  layout. Fixed by neutralizing the legacy menu (`width:0; display:none`) and giving our
  sidebar its own collapse logic + content margins. Don't reintroduce visible legacy menu.
- **Disappearing icons:** caused by treating all icons as one format. Use the
  FontAwesome-vs-sprite detection helpers.
- **Edit Modules gear does nothing:** the legacy `#side-menu-component` mount was removed or
  the Vue instance wasn't found — keep `templates/side-menu.html` mounted.
- **Dark mode not applying to sidebar/second pane:** themed-color rules overriding dark via
  source order — see §7; keep the authoritative `!important` dark block last.
- **"My SCSS change didn't show up":** you forgot `bench build` (and/or the browser cached
  the old hashed bundle). Run build + clear-cache + hard refresh.
- **Editing the wrong app:** changes in `datavalue_theme_15` won't show on `site1.local`
  (which runs `riyalsystem_theme`).

---

## 12. Quick reference — where things live

| I want to… | Go to |
| --- | --- |
| Change sidebar layout/behavior | `public/js/customizations/sidebar/sidebar-nav.js` |
| Change sidebar/second-pane styles | `public/scss/partials/_sidebar-nav.scss` |
| Change what workspaces show in the menu | `desktop.py` |
| Add/edit a whitelisted API | `api.py` |
| Add an asset (JS/CSS) to the desk | `www/app.html` (+ `hooks.py` for bundles) |
| Change body classes / CSS vars at boot | `www/app.html` + `www/app.py` |
| Apply settings at runtime | `public/js/customizations/theme/dark-mode.js` |
| Dark mode variable remaps | `public/scss/partials/_dark-style.scss` |
| Themed-color layout classes | `public/scss/partials/_layouts-color.scss` |
| Theme config fields | `riyalsystem_theme/doctype/theme_settings/theme_settings.json` |
| Custom Workspace fields | `riyalsystem_theme/custom/workspace.json` |

---

## 13. Standard commands

```bash
# from bench root: /home/frappe/frappe-bench
bench build --app riyalsystem_theme          # compile SCSS + bundle JS
bench --site site1.local clear-cache         # clear server cache
bench --site site1.local migrate             # apply doctype/schema/fixture changes
bench restart                                # restart services if needed
bench --site site1.local console             # python REPL for quick checks
```

When you finish a UI change, the minimum loop is:
**edit → `bench build --app riyalsystem_theme` → `bench --site site1.local clear-cache` → hard refresh browser.**
