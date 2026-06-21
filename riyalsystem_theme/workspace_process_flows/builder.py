"""Build Custom HTML Block content from flow configuration."""

import html

from riyalsystem_theme.workspace_process_flows.flows_config import (
	ARROW_SVG,
	ICONS,
	PROCESS_FLOWS,
	SHARED_CSS,
	SHARED_JS,
)


def build_block_content(flow_key):
	"""Return html, css, js dict for a process flow."""
	flow = PROCESS_FLOWS[flow_key]
	return {
		"html": build_html(flow),
		"css": SHARED_CSS,
		"js": SHARED_JS,
	}


def build_html(flow):
	workspace = html.escape(flow.get("workspace", "").lower())
	compact = ""
	if not flow.get("flows") and len(flow.get("steps", [])) > 5:
		compact = " rst-wpf--compact"

	parts = [
		f'<div class="rst-wpf rst-wpf--{workspace}{compact}">',
		'<div class="rst-wpf__header">',
		'<div class="rst-wpf__header-text">',
		f'<h3 class="rst-wpf__title">{html.escape(flow["title"])}</h3>',
		f'<p class="rst-wpf__subtitle">{html.escape(flow["subtitle"])}</p>',
		"</div></div>",
	]

	if flow.get("flows"):
		parts.append('<div class="rst-wpf__sections">')
		for section in flow["flows"]:
			parts.extend(_build_section(section))
		parts.append("</div>")
	else:
		parts.extend(_build_track(flow["steps"], flow["title"]))

	if flow.get("footer"):
		parts.append(f'<p class="rst-wpf__footer">{html.escape(flow["footer"])}</p>')

	parts.append("</div>")
	return "\n".join(parts)


def _build_section(section):
	parts = ['<div class="rst-wpf__section">', '<div class="rst-wpf__section-head">']
	parts.append(f'<h4 class="rst-wpf__section-title">{html.escape(section["title"])}</h4>')
	if section.get("description"):
		parts.append(f'<p class="rst-wpf__section-desc">{html.escape(section["description"])}</p>')
	parts.append("</div>")
	parts.extend(_build_track(section["steps"], section["title"]))
	parts.append("</div>")
	return parts


def _build_track(steps, label):
	compact = " rst-wpf--compact" if len(steps) > 5 else ""
	parts = [
		f'<div class="rst-wpf__track{compact}" role="list" aria-label="{html.escape(label)} steps">',
	]

	for index, step in enumerate(steps, start=1):
		if index > 1:
			parts.append(f'<div class="rst-wpf__arrow" aria-hidden="true">{ARROW_SVG}</div>')

		icon_path = ICONS.get(step.get("icon", "document"), ICONS["document"])
		doctype = html.escape(step["doctype"])
		step_label = html.escape(step["label"])

		parts.append(
			f'<div class="rst-wpf__step" role="listitem" data-doctype="{doctype}" tabindex="0">'
			f'<span class="rst-wpf__step-num">{index}</span>'
			f'<div class="rst-wpf__step-icon" aria-hidden="true">'
			f'<svg viewBox="0 0 24 24"><path d="{icon_path}"/></svg>'
			f"</div>"
			f'<span class="rst-wpf__step-label">{step_label}</span>'
			f"</div>"
		)

	parts.append("</div>")
	return parts


def get_flow_key_by_block_name(block_name):
	for key, flow in PROCESS_FLOWS.items():
		if flow["block_name"] == block_name:
			return key
	return None
