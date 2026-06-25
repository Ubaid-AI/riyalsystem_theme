"""Attach process-flow Custom HTML Blocks to ERPNext workspaces."""

from __future__ import annotations

import json
import re

import frappe

from riyalsystem_theme.workspace_process_flows.sync import sync_blocks

# Buying / Selling only — auto-placed on theme install (see module_flows for all blocks).
WORKSPACE_BLOCK_ASSIGNMENTS = (
	{
		"workspace": "Buying",
		"block_name": "RST Buying Process Flow",
		"before_header": "Your Shortcuts",
		"flow_key": "buying",
	},
	{
		"workspace": "Selling",
		"block_name": "RST Selling Process Flow",
		"before_header": "Quick Access",
		"flow_key": "selling",
	},
)


def sync_workspace_assignments():
	"""Ensure Buying/Selling workspaces show their process-flow blocks in layout."""
	sync_blocks()

	results = []
	for assignment in WORKSPACE_BLOCK_ASSIGNMENTS:
		results.append(_assign_block_to_workspace(assignment))

	if any(item.get("updated") for item in results):
		frappe.db.commit()
		frappe.clear_cache(doctype="Workspace")

	return results


def _assign_block_to_workspace(assignment: dict) -> dict:
	workspace_name = assignment["workspace"]
	block_name = assignment["block_name"]
	header_text = assignment["before_header"]
	result = {
		"workspace": workspace_name,
		"block_name": block_name,
		"updated": False,
		"skipped": None,
	}

	if not frappe.db.exists("Workspace", workspace_name):
		result["skipped"] = "workspace_not_found"
		return result

	if not frappe.db.exists("Custom HTML Block", block_name):
		result["skipped"] = "block_not_found"
		return result

	content_updated = _ensure_block_in_content(workspace_name, block_name, header_text)
	child_updated = _ensure_custom_block_row(workspace_name, block_name)

	result["updated"] = content_updated or child_updated
	return result


def _ensure_custom_block_row(workspace_name: str, block_name: str) -> bool:
	if frappe.db.exists(
		"Workspace Custom Block",
		{"parent": workspace_name, "custom_block_name": block_name},
	):
		return False

	max_idx = frappe.db.sql(
		"""
		SELECT COALESCE(MAX(idx), 0)
		FROM `tabWorkspace Custom Block`
		WHERE parent = %s
		""",
		workspace_name,
	)[0][0]

	frappe.get_doc(
		{
			"doctype": "Workspace Custom Block",
			"parent": workspace_name,
			"parenttype": "Workspace",
			"parentfield": "custom_blocks",
			"custom_block_name": block_name,
			"label": block_name,
			"idx": max_idx + 1,
		}
	).insert(ignore_permissions=True)
	return True


def _ensure_block_in_content(
	workspace_name: str, block_name: str, before_header: str
) -> bool:
	raw_content = frappe.db.get_value("Workspace", workspace_name, "content") or "[]"

	try:
		blocks = json.loads(raw_content)
	except json.JSONDecodeError:
		blocks = []

	if not isinstance(blocks, list):
		return False

	new_blocks, changed = _insert_or_move_custom_block(blocks, block_name, before_header)
	if not changed:
		return False

	frappe.db.set_value(
		"Workspace",
		workspace_name,
		"content",
		json.dumps(new_blocks, separators=(",", ":")),
		update_modified=False,
	)
	return True


def _find_header_index(blocks: list, header_text: str) -> int | None:
	needle = header_text.strip().lower()
	for index, block in enumerate(blocks):
		if block.get("type") != "header":
			continue
		text = _plain_header_text(block.get("data", {}).get("text", ""))
		if needle in text.lower():
			return index
	return None


def _plain_header_text(html_text: str) -> str:
	text = re.sub(r"<[^>]+>", " ", html_text or "")
	return re.sub(r"\s+", " ", text).strip()


def _is_custom_block(block: dict, block_name: str) -> bool:
	return (
		block.get("type") == "custom_block"
		and block.get("data", {}).get("custom_block_name") == block_name
	)


def _insert_or_move_custom_block(
	blocks: list, block_name: str, before_header: str
) -> tuple[list, bool]:
	header_index = _find_header_index(blocks, before_header)
	if header_index is None:
		return blocks, False

	if header_index > 0 and _is_custom_block(blocks[header_index - 1], block_name):
		return blocks, False

	existing = None
	filtered = []

	for block in blocks:
		if _is_custom_block(block, block_name):
			existing = block
			continue
		filtered.append(block)

	header_index = _find_header_index(filtered, before_header)
	if header_index is None:
		return blocks, False

	block_to_insert = existing or {
		"id": frappe.generate_hash(length=10),
		"type": "custom_block",
		"data": {"custom_block_name": block_name, "col": 12},
	}

	filtered.insert(header_index, block_to_insert)
	return filtered, True
