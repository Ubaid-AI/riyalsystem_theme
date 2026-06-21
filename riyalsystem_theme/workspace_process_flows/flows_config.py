"""Shared CSS for all workspace process flow blocks."""

SHARED_CSS = """:host {
	display: block;
	width: 100%;
	font-family: var(--font-stack, Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif);
}

.rst-wpf {
	--wpf-primary: var(--primary, #2490ef);
	--wpf-bg: var(--fg-color, #fff);
	--wpf-card: var(--card-bg, #fff);
	--wpf-border: var(--border-color, #e2e8f0);
	--wpf-muted: var(--text-muted, #64748b);
	--wpf-text: var(--text-color, #171717);
	--wpf-icon-bg: color-mix(in srgb, var(--wpf-primary) 10%, var(--wpf-card));
	--wpf-icon-hover: color-mix(in srgb, var(--wpf-primary) 18%, var(--wpf-card));

	box-sizing: border-box;
	padding: 14px 16px;
	background: var(--wpf-bg);
	border: 1px solid var(--wpf-border);
	border-radius: 10px;
}

.rst-wpf__header { margin-bottom: 12px; }

.rst-wpf__title {
	margin: 0 0 2px;
	font-size: 14px;
	font-weight: 700;
	line-height: 1.3;
	color: var(--wpf-text);
}

.rst-wpf__subtitle {
	margin: 0;
	font-size: 11px;
	line-height: 1.4;
	color: var(--wpf-muted);
}

.rst-wpf__track {
	display: flex;
	align-items: center;
	gap: 0;
	overflow-x: auto;
	padding: 2px 0;
	-webkit-overflow-scrolling: touch;
	scrollbar-width: thin;
}

.rst-wpf__step {
	position: relative;
	flex: 1 1 0;
	min-width: 88px;
	max-width: 120px;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 7px;
	padding: 10px 8px 9px;
	background: var(--wpf-card);
	border: 1px solid var(--wpf-border);
	border-radius: 8px;
	cursor: pointer;
	outline: none;
	transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.rst-wpf--compact .rst-wpf__step,
.rst-wpf__track.rst-wpf--compact .rst-wpf__step {
	min-width: 72px;
	max-width: 98px;
	padding: 9px 6px 8px;
	gap: 6px;
}

.rst-wpf--compact .rst-wpf__step-icon,
.rst-wpf__track.rst-wpf--compact .rst-wpf__step-icon { width: 32px; height: 32px; }
.rst-wpf--compact .rst-wpf__step-icon svg,
.rst-wpf__track.rst-wpf--compact .rst-wpf__step-icon svg { width: 16px; height: 16px; }
.rst-wpf--compact .rst-wpf__step-label,
.rst-wpf__track.rst-wpf--compact .rst-wpf__step-label { font-size: 10px; }
.rst-wpf--compact .rst-wpf__arrow,
.rst-wpf__track.rst-wpf--compact .rst-wpf__arrow { width: 14px; }
.rst-wpf--compact .rst-wpf__arrow svg,
.rst-wpf__track.rst-wpf--compact .rst-wpf__arrow svg { width: 14px; height: 14px; }

.rst-wpf__step:hover,
.rst-wpf__step:focus-visible {
	border-color: color-mix(in srgb, var(--wpf-primary) 50%, var(--wpf-border));
	box-shadow: 0 4px 14px color-mix(in srgb, var(--wpf-primary) 12%, transparent);
	transform: translateY(-1px);
}

.rst-wpf__step:focus-visible {
	box-shadow:
		0 4px 14px color-mix(in srgb, var(--wpf-primary) 12%, transparent),
		0 0 0 2px color-mix(in srgb, var(--wpf-primary) 20%, transparent);
}

.rst-wpf__step-num {
	position: absolute;
	top: 6px;
	right: 6px;
	min-width: 16px;
	height: 16px;
	padding: 0 4px;
	border-radius: 4px;
	font-size: 9px;
	font-weight: 700;
	line-height: 14px;
	text-align: center;
	color: var(--wpf-primary);
	background: var(--wpf-card);
	border: 1px solid color-mix(in srgb, var(--wpf-primary) 35%, var(--wpf-border));
	box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
	z-index: 1;
}

.rst-wpf__step-icon {
	width: 36px;
	height: 36px;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: var(--wpf-icon-bg);
	border: 1px solid color-mix(in srgb, var(--wpf-primary) 22%, var(--wpf-border));
	transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}

.rst-wpf__step-icon svg { width: 18px; height: 18px; display: block; }
.rst-wpf__step-icon svg path { fill: var(--wpf-primary); transition: fill 0.15s ease; }

.rst-wpf__step:hover .rst-wpf__step-icon,
.rst-wpf__step:focus-visible .rst-wpf__step-icon {
	background: var(--wpf-icon-hover);
	border-color: color-mix(in srgb, var(--wpf-primary) 45%, var(--wpf-border));
	transform: scale(1.04);
}

.rst-wpf__step:hover .rst-wpf__step-icon svg path,
.rst-wpf__step:focus-visible .rst-wpf__step-icon svg path {
	fill: color-mix(in srgb, var(--wpf-primary) 88%, #000);
}

.rst-wpf__step-label {
	font-size: 11px;
	font-weight: 600;
	line-height: 1.25;
	color: var(--wpf-text);
	text-align: center;
	word-break: break-word;
}

.rst-wpf__step:hover .rst-wpf__step-label,
.rst-wpf__step:focus-visible .rst-wpf__step-label { color: var(--wpf-primary); }

.rst-wpf__arrow {
	flex: 0 0 auto;
	display: flex;
	align-items: center;
	justify-content: center;
	width: 18px;
	color: var(--wpf-muted);
	opacity: 0.55;
}

.rst-wpf__arrow svg { width: 16px; height: 16px; display: block; }
.rst-wpf__arrow svg path { fill: currentColor; }

.rst-wpf__sections {
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.rst-wpf__section {
	padding-top: 10px;
	border-top: 1px solid color-mix(in srgb, var(--wpf-border) 85%, transparent);
}

.rst-wpf__section:first-child {
	padding-top: 0;
	border-top: none;
}

.rst-wpf__section-head {
	margin-bottom: 8px;
}

.rst-wpf__section-title {
	margin: 0 0 2px;
	font-size: 11px;
	font-weight: 700;
	color: var(--wpf-text);
}

.rst-wpf__section-desc {
	margin: 0;
	font-size: 10px;
	line-height: 1.35;
	color: var(--wpf-muted);
}

.rst-wpf__footer {
	margin-top: 10px;
	padding-top: 8px;
	border-top: 1px solid var(--wpf-border);
	font-size: 10px;
	color: var(--wpf-muted);
	text-align: center;
}

@media (max-width: 900px) {
	.rst-wpf { padding: 12px; }
	.rst-wpf__step { min-width: 78px; max-width: 100px; padding: 9px 6px 8px; }
	.rst-wpf__step-icon { width: 32px; height: 32px; }
	.rst-wpf__step-icon svg { width: 16px; height: 16px; }
	.rst-wpf__step-label { font-size: 10px; }
	.rst-wpf__arrow { width: 14px; }
	.rst-wpf--compact .rst-wpf__step,
	.rst-wpf__track.rst-wpf--compact .rst-wpf__step { min-width: 68px; max-width: 88px; }
}

@media (max-width: 560px) {
	.rst-wpf__step { min-width: 72px; }
	.rst-wpf__step-num { top: 4px; right: 4px; }
	.rst-wpf--compact .rst-wpf__step,
	.rst-wpf__track.rst-wpf--compact .rst-wpf__step { min-width: 64px; }
}
"""

SHARED_JS = """(function () {
	const wpf = root_element.querySelector(".rst-wpf");
	const steps = root_element.querySelectorAll(".rst-wpf__step[data-doctype]");

	function sync_theme_colors() {
		if (!wpf) return;
		const source = document.body || document.documentElement;
		const computed = getComputedStyle(source);
		const theme_vars = {
			"--wpf-primary": "--primary",
			"--wpf-bg": "--fg-color",
			"--wpf-card": "--card-bg",
			"--wpf-border": "--border-color",
			"--wpf-muted": "--text-muted",
			"--wpf-text": "--text-color",
		};
		Object.entries(theme_vars).forEach(([target, source_var]) => {
			const value = computed.getPropertyValue(source_var).trim();
			if (value) wpf.style.setProperty(target, value);
		});
	}

	sync_theme_colors();

	if (typeof MutationObserver !== "undefined" && document.body) {
		new MutationObserver(sync_theme_colors).observe(document.body, {
			attributes: true,
			attributeFilter: ["class", "style", "data-theme-color"],
		});
	}

	steps.forEach((step) => {
		const doctype = step.dataset.doctype;
		step.addEventListener("click", () => {
			if (typeof frappe === "undefined") return;
			if (frappe.new_doc) frappe.new_doc(doctype);
			else frappe.set_route("Form", doctype, "new");
		});
		step.addEventListener("keydown", (event) => {
			if (event.key === "Enter" || event.key === " ") {
				event.preventDefault();
				step.click();
			}
		});
	});
})();
"""

ARROW_SVG = '<svg viewBox="0 0 24 24"><path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>'

ICONS = {
	"document": "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8 13h8v2H8v-2zm0 4h5v2H8v-2z",
	"cart": "M7 4h10l1 2h3a1 1 0 0 1 1 1v2H3V7a1 1 0 0 1 1-1h3l1-2zm-1 8h14l-1.5 8H7.5L6 12zm2 2v2h2v-2H8zm4 0v2h2v-2h-2z",
	"truck": "M3 6h11v9H3V6zm12 0h2.5l2.5 3v6H15V6zm-9 11h12a2 2 0 0 0 2-2v-1H3v1a2 2 0 0 0 2 2zm2-8h2v2H8v-2zm4 0h2v2h-2v-2z",
	"invoice": "M6 2h9l5 5v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm8 1.5V8h4.5L14 3.5zM8 12h8v2H8v-2zm0 4h8v2H8v-2z",
	"payment": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1.41 16.09V20h-2.67v-1.93c-1.71-.36-3.16-1.46-3.27-3.4h1.96c.1 1.05.82 1.87 2.65 1.87 1.96 0 2.4-.98 2.4-1.59 0-.83-.44-1.61-2.67-2.14-2.48-.6-4.18-1.62-4.18-3.67 0-1.72 1.39-2.84 3.11-3.21V4h2.67v1.95c1.86.45 2.79 1.86 2.85 3.39H14.3c-.05-1.11-.64-1.87-2.22-1.87-1.5 0-2.4.68-2.4 1.64 0 .84.65 1.39 2.67 1.91s4.18 1.39 4.18 3.91c-.01 1.83-1.38 2.83-3.12 3.16z",
	"lead": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
	"opportunity": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
	"material": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z",
	"rfq": "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm4 18H6V4h7v5h5v11zM8 15h8v2H8v-2zm0-4h8v2H8v-2z",
	"supplier": "M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10z",
	"purchase": "M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49A1 1 0 0 0 20 4H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z",
	"receipt": "M18 17H6v-2h12v2zm0-4H6v-2h12v2zm0-4H6V7h12v2zM3 22l1.5-1.5L6 22l1.5-1.5L9 22l1.5-1.5L12 22l1.5-1.5L15 22l1.5-1.5L18 22l1.5-1.5L21 22V2l-1.5 1.5L18 2l-1.5 1.5L15 2l-1.5 1.5L12 2l-1.5 1.5L9 2 7.5 3.5 6 2 4.5 3.5 3 2v20z",
	"stock": "M20 2H4a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm-8 2h8v4h-8V4zm8 16H4V10h16v10z",
	"pick": "M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 16H5V9h14v11z",
	"bom": "M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z",
	"work_order": "M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z",
	"job_card": "M20 4H4c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm-5 14H4v-4h11v4zm0-5H4V9h11v4zm5 5h-4V9h4v9z",
	"journal": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z",
	"project": "M10 4H4c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2h-8l-2-2z",
	"task": "M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z",
	"timesheet": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z",
	"employee": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
	"job_opening": "M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z",
	"applicant": "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
	"interview": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z",
	"issue": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z",
	"maintenance": "M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z",
	"warranty": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z",
	"quality": "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27z",
	"inspection": "M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z",
	"action": "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z",
	"feedback": "M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z",
	"asset": "M18 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 14H6V6h12v12zM8 8h8v8H8V8z",
	"movement": "M16 17.01V10h-2v7.01h-3L15 21l4-3.99h-3zM9 3.99v7H7V3.99H4L8 0l4 3.99h-3z",
	"depreciation": "M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.9-4.71-3.9-2.83 0-4.87 1.38-4.87 3.83 0 2.5 1.66 3.73 4.03 4.32 2.67.73 3.2 1.58 3.2 2.65 0 1.22-1.01 1.95-2.75 1.95-2.19 0-2.96-.92-3.06-2.1H4.89c.09 2.01 1.65 4.01 5.36 4.01 3.04 0 5.09-1.55 5.09-4.01 0-2.65-1.73-3.86-4.54-4.36z",
	"repair": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z",
	"prospect": "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
	"customer": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-8 8v-1.5c0-1.67 3.33-2.5 8-2.5s8 .83 8 2.5V20H4z",
	"campaign": "M18 11v2h4v-2h-4zm-2 6.61c.96.71 2.21 1.65 3.2 2.39.4-.53.8-1.08 1.2-1.62-.6-.45-1.17-.86-1.68-1.23l-1.32 1.46zM20.4 5.6c-.4-.53-.8-1.08-1.2-1.62-.99.74-2.24 1.68-3.2 2.39l1.32 1.46c.51-.37 1.08-.78 1.68-1.23zM4 9c-1.1 0-2 .9-2 2v2c0 1.1.9 2 2 2h1v4h2v-4h1l5 3V6L8 9H4z",
	"communication": "M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z",
	"contract": "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8 12h8v2H8v-2zm0 4h5v2H8v-2z",
	"production_plan": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z",
	"bank": "M4 10v7h3v-7H4zm6 0v7h3v-7h-3zm6 0v7h3v-7h-3zm-9-6L2 8v2h20V8l-9-4z",
	"reconciliation": "M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46A7.93 7.93 0 0 0 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74A7.93 7.93 0 0 0 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z",
	"dunning": "M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z",
	"closing": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l7.59-7.59L21 8l-9 9z",
	"job_offer": "M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z",
	"onboarding": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z",
	"leave": "M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7v-5z",
	"attendance": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z",
	"payroll": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1.41 16.09V20h-2.67v-1.93c-1.71-.36-3.16-1.46-3.27-3.4h1.96c.1 1.05.82 1.87 2.65 1.87 1.96 0 2.4-.98 2.4-1.59 0-.83-.44-1.61-2.67-2.14-2.48-.6-4.18-1.62-4.18-3.67 0-1.72 1.39-2.84 3.11-3.21V4h2.67v1.95c1.86.45 2.79 1.86 2.85 3.39H14.3c-.05-1.11-.64-1.87-2.22-1.87-1.5 0-2.4.68-2.4 1.64 0 .84.65 1.39 2.67 1.91s4.18 1.39 4.18 3.91c-.01 1.83-1.38 2.83-3.12 3.16z",
	"salary": "M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.9-4.71-3.9-2.83 0-4.87 1.38-4.87 3.83 0 2.5 1.66 3.73 4.03 4.32 2.67.73 3.2 1.58 3.2 2.65 0 1.22-1.01 1.95-2.75 1.95-2.19 0-2.96-.92-3.06-2.1H4.89c.09 2.01 1.65 4.01 5.36 4.01 3.04 0 5.09-1.55 5.09-4.01 0-2.65-1.73-3.86-4.54-4.36z",
	"sla": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z",
}

from riyalsystem_theme.workspace_process_flows.module_flows import PROCESS_FLOWS  # noqa: E402, F401


def get_all_block_names():
	return [flow["block_name"] for flow in PROCESS_FLOWS.values()]
