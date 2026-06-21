"""API for the visual document flow tracker."""

import frappe

from riyalsystem_theme.document_flow.flows import DOCUMENT_FLOWS, get_flow_for_doctype
from riyalsystem_theme.document_flow.links import get_linked_documents


@frappe.whitelist()
def get_document_flow(doctype, name=None, is_new=None):
	"""Return flow steps with status and linked documents for a given record."""
	if not doctype:
		return {}

	if frappe.sbool(is_new) or not name:
		return get_document_flow_draft(doctype)

	doc = frappe.get_doc(doctype, name)
	doc.check_permission()

	flow_info = get_flow_for_doctype(doctype, doc)
	if not flow_info:
		return {}

	flow_id, flow, current_index = flow_info

	steps = []
	for idx, step in enumerate(flow["steps"]):
		step_doctype = step["doctype"]
		is_current = idx == current_index

		if is_current:
			linked_names = [name]
		else:
			linked_names = get_linked_documents(doctype, name, step_doctype)

		make_method = (step.get("make_methods") or {}).get(doctype)
		can_create = bool(make_method) and not linked_names and _can_create(step_doctype)

		if is_current:
			status = "current"
		elif linked_names:
			status = "completed"
		else:
			status = "pending"

		step_data = {
			"doctype": step_doctype,
			"label": step.get("label") or step_doctype,
			"status": status,
			"count": len(linked_names),
			"names": linked_names,
			"can_create": can_create,
			"is_current": is_current,
			"is_navigable": bool(linked_names) and not is_current,
		}

		if can_create:
			step_data["make_method"] = make_method
			if step.get("create_action"):
				step_data["create_action"] = step["create_action"]
			if step.get("trigger"):
				step_data["trigger"] = step["trigger"]

		steps.append(step_data)

	return {
		"flow_id": flow_id,
		"flow_label": flow["label"],
		"current_doctype": doctype,
		"current_name": name,
		"is_unsaved": False,
		"steps": steps,
	}


@frappe.whitelist()
def get_document_flow_draft(doctype):
	"""Return flow steps for a new unsaved document."""
	flow_info = get_flow_for_doctype(doctype)
	if not flow_info:
		return {}

	flow_id, flow, current_index = flow_info
	steps = []

	for idx, step in enumerate(flow["steps"]):
		is_current = idx == current_index
		steps.append(
			{
				"doctype": step["doctype"],
				"label": step.get("label") or step["doctype"],
				"status": "draft" if is_current else "pending",
				"count": 0,
				"names": [],
				"can_create": False,
				"is_current": is_current,
				"is_unsaved": is_current,
				"is_navigable": False,
			}
		)

	return {
		"flow_id": flow_id,
		"flow_label": flow["label"],
		"current_doctype": doctype,
		"current_name": None,
		"is_unsaved": True,
		"steps": steps,
	}


def _can_create(doctype):
	return frappe.has_permission(doctype, "create")


@frappe.whitelist()
def get_flow_config():
	"""Return flow configuration for client-side reference."""
	return DOCUMENT_FLOWS
