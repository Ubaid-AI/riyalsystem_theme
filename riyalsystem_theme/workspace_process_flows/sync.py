"""Sync Custom HTML Block records from workspace process flow templates."""

import json
from pathlib import Path

import frappe

from riyalsystem_theme.workspace_process_flows.builder import build_block_content
from riyalsystem_theme.workspace_process_flows.flows_config import PROCESS_FLOWS, get_all_block_names

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def sync_blocks():
	"""Create or update all process flow Custom HTML Block records."""
	for flow_key, flow in PROCESS_FLOWS.items():
		_upsert_block(flow["block_name"], flow_key)


def export_fixtures():
	"""Write all block records to fixtures/custom_html_block.json."""
	records = []
	for block_name in get_all_block_names():
		if frappe.db.exists("Custom HTML Block", block_name):
			doc = frappe.get_doc("Custom HTML Block", block_name)
			data = doc.as_dict()
			for key in list(data.keys()):
				if key.startswith("_"):
					data.pop(key, None)
			records.append(data)

	FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
	fixture_path = FIXTURES_DIR / "custom_html_block.json"
	with open(fixture_path, "w", encoding="utf-8") as handle:
		json.dump(records, handle, indent=1, default=str)

	return fixture_path


def _upsert_block(block_name, flow_key):
	content = build_block_content(flow_key)

	if frappe.db.exists("Custom HTML Block", block_name):
		doc = frappe.get_doc("Custom HTML Block", block_name)
		doc.html = content["html"]
		doc.style = content["css"]
		doc.script = content["js"]
		doc.private = 0
		doc.save(ignore_permissions=True)
		return

	frappe.get_doc(
		{
			"doctype": "Custom HTML Block",
			"name": block_name,
			"html": content["html"],
			"style": content["css"],
			"script": content["js"],
			"private": 0,
		}
	).insert(ignore_permissions=True)
