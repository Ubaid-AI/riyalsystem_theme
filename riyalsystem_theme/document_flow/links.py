"""Resolve linked documents between doctypes for the process tracker."""

import frappe

# Link resolvers keyed by (source_doctype, target_doctype)
LINK_RESOLVERS = {
	("Quotation", "Sales Order"): [
		{
			"type": "child",
			"parent_doctype": "Sales Order",
			"child_doctype": "Sales Order Item",
			"link_field": "prevdoc_docname",
		}
	],
	("Sales Order", "Quotation"): [
		{
			"type": "child_rows",
			"child_doctype": "Sales Order Item",
			"field": "prevdoc_docname",
		}
	],
	("Sales Order", "Delivery Note"): [
		{
			"type": "child",
			"parent_doctype": "Delivery Note",
			"child_doctype": "Delivery Note Item",
			"link_field": "against_sales_order",
		}
	],
	("Delivery Note", "Sales Order"): [
		{
			"type": "child_rows",
			"child_doctype": "Delivery Note Item",
			"field": "against_sales_order",
		}
	],
	("Sales Order", "Sales Invoice"): [
		{
			"type": "child",
			"parent_doctype": "Sales Invoice",
			"child_doctype": "Sales Invoice Item",
			"link_field": "sales_order",
		}
	],
	("Delivery Note", "Sales Invoice"): [
		{
			"type": "child",
			"parent_doctype": "Sales Invoice",
			"child_doctype": "Sales Invoice Item",
			"link_field": "delivery_note",
		}
	],
	("Sales Invoice", "Sales Order"): [
		{
			"type": "child_rows",
			"child_doctype": "Sales Invoice Item",
			"field": "sales_order",
		}
	],
	("Sales Invoice", "Delivery Note"): [
		{
			"type": "child_rows",
			"child_doctype": "Sales Invoice Item",
			"field": "delivery_note",
		}
	],
	("Sales Invoice", "Payment Entry"): [
		{
			"type": "child",
			"parent_doctype": "Payment Entry",
			"child_doctype": "Payment Entry Reference",
			"link_field": "reference_name",
			"filters": {"reference_doctype": "Sales Invoice"},
		}
	],
	("Sales Order", "Payment Entry"): [
		{
			"type": "child",
			"parent_doctype": "Payment Entry",
			"child_doctype": "Payment Entry Reference",
			"link_field": "reference_name",
			"filters": {"reference_doctype": "Sales Order"},
		}
	],
	("Payment Entry", "Sales Invoice"): [
		{
			"type": "child_rows",
			"child_doctype": "Payment Entry Reference",
			"field": "reference_name",
			"filters": {"reference_doctype": "Sales Invoice"},
		}
	],
	("Payment Entry", "Sales Order"): [
		{
			"type": "child_rows",
			"child_doctype": "Payment Entry Reference",
			"field": "reference_name",
			"filters": {"reference_doctype": "Sales Order"},
		},
		{"type": "chain", "via": ("Payment Entry", "Sales Invoice"), "then": ("Sales Invoice", "Sales Order")},
	],
	("Payment Entry", "Delivery Note"): [
		{"type": "chain", "via": ("Payment Entry", "Sales Invoice"), "then": ("Sales Invoice", "Delivery Note")}
	],
	("Payment Entry", "Quotation"): [
		{"type": "chain", "via": ("Payment Entry", "Sales Order"), "then": ("Sales Order", "Quotation")}
	],
	("Sales Invoice", "Quotation"): [
		{"type": "chain", "via": ("Sales Invoice", "Sales Order"), "then": ("Sales Order", "Quotation")}
	],
	("Delivery Note", "Quotation"): [
		{"type": "chain", "via": ("Delivery Note", "Sales Order"), "then": ("Sales Order", "Quotation")}
	],
	("Sales Order", "Lead"): [
		{"type": "chain", "via": ("Sales Order", "Quotation"), "then": ("Quotation", "Lead")}
	],
	("Sales Order", "Opportunity"): [
		{"type": "chain", "via": ("Sales Order", "Quotation"), "then": ("Quotation", "Opportunity")}
	],
	("Lead", "Opportunity"): [
		{
			"type": "field",
			"doctype": "Opportunity",
			"field": "party_name",
			"filters": {"opportunity_from": "Lead"},
		}
	],
	("Opportunity", "Lead"): [
		{
			"type": "self_field",
			"field": "party_name",
			"filters": {"opportunity_from": "Lead"},
		}
	],
	("Lead", "Quotation"): [
		{
			"type": "field",
			"doctype": "Quotation",
			"field": "party_name",
			"filters": {"quotation_to": "Lead"},
		}
	],
	("Opportunity", "Quotation"): [
		{"type": "field", "doctype": "Quotation", "field": "opportunity"},
		{
			"type": "child",
			"parent_doctype": "Quotation",
			"child_doctype": "Quotation Item",
			"link_field": "prevdoc_docname",
		},
	],
	("Quotation", "Opportunity"): [
		{"type": "self_field", "field": "opportunity"},
	],
	("Quotation", "Lead"): [
		{
			"type": "self_field",
			"field": "party_name",
			"filters": {"quotation_to": "Lead"},
		}
	],
	("Material Request", "Request for Quotation"): [
		{
			"type": "child",
			"parent_doctype": "Request for Quotation",
			"child_doctype": "Request for Quotation Item",
			"link_field": "material_request",
		}
	],
	("Request for Quotation", "Material Request"): [
		{
			"type": "child_rows",
			"child_doctype": "Request for Quotation Item",
			"field": "material_request",
		}
	],
	("Request for Quotation", "Supplier Quotation"): [
		{
			"type": "child",
			"parent_doctype": "Supplier Quotation",
			"child_doctype": "Supplier Quotation Item",
			"link_field": "request_for_quotation",
		}
	],
	("Supplier Quotation", "Request for Quotation"): [
		{
			"type": "child_rows",
			"child_doctype": "Supplier Quotation Item",
			"field": "request_for_quotation",
		}
	],
	("Supplier Quotation", "Purchase Order"): [
		{
			"type": "child",
			"parent_doctype": "Purchase Order",
			"child_doctype": "Purchase Order Item",
			"link_field": "supplier_quotation",
		}
	],
	("Purchase Order", "Supplier Quotation"): [
		{
			"type": "child_rows",
			"child_doctype": "Purchase Order Item",
			"field": "supplier_quotation",
		}
	],
	("Material Request", "Purchase Order"): [
		{
			"type": "child",
			"parent_doctype": "Purchase Order",
			"child_doctype": "Purchase Order Item",
			"link_field": "material_request",
		}
	],
	("Purchase Order", "Material Request"): [
		{
			"type": "child_rows",
			"child_doctype": "Purchase Order Item",
			"field": "material_request",
		}
	],
	("Purchase Order", "Purchase Receipt"): [
		{
			"type": "child",
			"parent_doctype": "Purchase Receipt",
			"child_doctype": "Purchase Receipt Item",
			"link_field": "purchase_order",
		}
	],
	("Purchase Receipt", "Purchase Order"): [
		{
			"type": "child_rows",
			"child_doctype": "Purchase Receipt Item",
			"field": "purchase_order",
		}
	],
	("Purchase Order", "Purchase Invoice"): [
		{
			"type": "child",
			"parent_doctype": "Purchase Invoice",
			"child_doctype": "Purchase Invoice Item",
			"link_field": "purchase_order",
		}
	],
	("Purchase Receipt", "Purchase Invoice"): [
		{
			"type": "child",
			"parent_doctype": "Purchase Invoice",
			"child_doctype": "Purchase Invoice Item",
			"link_field": "purchase_receipt",
		}
	],
	("Purchase Invoice", "Purchase Order"): [
		{
			"type": "child_rows",
			"child_doctype": "Purchase Invoice Item",
			"field": "purchase_order",
		}
	],
	("Purchase Invoice", "Payment Entry"): [
		{
			"type": "child",
			"parent_doctype": "Payment Entry",
			"child_doctype": "Payment Entry Reference",
			"link_field": "reference_name",
			"filters": {"reference_doctype": "Purchase Invoice"},
		}
	],
	("Purchase Order", "Payment Entry"): [
		{
			"type": "child",
			"parent_doctype": "Payment Entry",
			"child_doctype": "Payment Entry Reference",
			"link_field": "reference_name",
			"filters": {"reference_doctype": "Purchase Order"},
		}
	],
	("Payment Entry", "Purchase Invoice"): [
		{
			"type": "child_rows",
			"child_doctype": "Payment Entry Reference",
			"field": "reference_name",
			"filters": {"reference_doctype": "Purchase Invoice"},
		}
	],
	("Payment Entry", "Purchase Order"): [
		{
			"type": "child_rows",
			"child_doctype": "Payment Entry Reference",
			"field": "reference_name",
			"filters": {"reference_doctype": "Purchase Order"},
		},
		{
			"type": "chain",
			"via": ("Payment Entry", "Purchase Invoice"),
			"then": ("Purchase Invoice", "Purchase Order"),
		},
	],
	("Payment Entry", "Purchase Receipt"): [
		{
			"type": "chain",
			"via": ("Payment Entry", "Purchase Invoice"),
			"then": ("Purchase Invoice", "Purchase Receipt"),
		},
		{
			"type": "chain",
			"via": ("Payment Entry", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Receipt"),
		},
	],
	("Payment Entry", "Supplier Quotation"): [
		{
			"type": "chain",
			"via": ("Payment Entry", "Purchase Order"),
			"then": ("Purchase Order", "Supplier Quotation"),
		}
	],
	("Payment Entry", "Request for Quotation"): [
		{
			"type": "chain",
			"via": ("Payment Entry", "Purchase Order"),
			"then": ("Purchase Order", "Request for Quotation"),
		}
	],
	("Payment Entry", "Material Request"): [
		{
			"type": "chain",
			"via": ("Payment Entry", "Purchase Order"),
			"then": ("Purchase Order", "Material Request"),
		}
	],
	("Purchase Order", "Request for Quotation"): [
		{
			"type": "chain",
			"via": ("Purchase Order", "Supplier Quotation"),
			"then": ("Supplier Quotation", "Request for Quotation"),
		}
	],
	("Purchase Invoice", "Material Request"): [
		{
			"type": "chain",
			"via": ("Purchase Invoice", "Purchase Order"),
			"then": ("Purchase Order", "Material Request"),
		}
	],
	("Purchase Receipt", "Material Request"): [
		{
			"type": "chain",
			"via": ("Purchase Receipt", "Purchase Order"),
			"then": ("Purchase Order", "Material Request"),
		}
	],
	("Purchase Invoice", "Request for Quotation"): [
		{
			"type": "chain",
			"via": ("Purchase Invoice", "Purchase Order"),
			"then": ("Purchase Order", "Request for Quotation"),
		}
	],
	("Purchase Invoice", "Supplier Quotation"): [
		{
			"type": "chain",
			"via": ("Purchase Invoice", "Purchase Order"),
			"then": ("Purchase Order", "Supplier Quotation"),
		}
	],
	("Purchase Receipt", "Supplier Quotation"): [
		{
			"type": "chain",
			"via": ("Purchase Receipt", "Purchase Order"),
			"then": ("Purchase Order", "Supplier Quotation"),
		}
	],
	("Purchase Receipt", "Request for Quotation"): [
		{
			"type": "chain",
			"via": ("Purchase Receipt", "Purchase Order"),
			"then": ("Purchase Order", "Request for Quotation"),
		}
	],
	# Chain hops for downstream steps when viewing an upstream document
	("Quotation", "Delivery Note"): [
		{"type": "chain", "via": ("Quotation", "Sales Order"), "then": ("Sales Order", "Delivery Note")}
	],
	("Quotation", "Sales Invoice"): [
		{"type": "chain", "via": ("Quotation", "Sales Order"), "then": ("Sales Order", "Sales Invoice")}
	],
	("Quotation", "Payment Entry"): [
		{"type": "chain", "via": ("Quotation", "Sales Invoice"), "then": ("Sales Invoice", "Payment Entry")}
	],
	("Sales Order", "Payment Entry"): [
		{"type": "chain", "via": ("Sales Order", "Sales Invoice"), "then": ("Sales Invoice", "Payment Entry")}
	],
	("Delivery Note", "Payment Entry"): [
		{"type": "chain", "via": ("Delivery Note", "Sales Invoice"), "then": ("Sales Invoice", "Payment Entry")}
	],
	("Material Request", "Supplier Quotation"): [
		{
			"type": "chain",
			"via": ("Material Request", "Request for Quotation"),
			"then": ("Request for Quotation", "Supplier Quotation"),
		}
	],
	("Material Request", "Purchase Order"): [
		{
			"type": "direct_child",
			"parent_doctype": "Purchase Order",
			"child_doctype": "Purchase Order Item",
			"link_field": "material_request",
		},
		{
			"type": "chain",
			"via": ("Material Request", "Supplier Quotation"),
			"then": ("Supplier Quotation", "Purchase Order"),
		},
	],
	("Request for Quotation", "Purchase Order"): [
		{
			"type": "chain",
			"via": ("Request for Quotation", "Supplier Quotation"),
			"then": ("Supplier Quotation", "Purchase Order"),
		}
	],
	("Material Request", "Purchase Receipt"): [
		{
			"type": "chain",
			"via": ("Material Request", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Receipt"),
		}
	],
	("Request for Quotation", "Purchase Receipt"): [
		{
			"type": "chain",
			"via": ("Request for Quotation", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Receipt"),
		}
	],
	("Supplier Quotation", "Purchase Receipt"): [
		{
			"type": "chain",
			"via": ("Supplier Quotation", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Receipt"),
		}
	],
	("Material Request", "Purchase Invoice"): [
		{
			"type": "chain",
			"via": ("Material Request", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Invoice"),
		}
	],
	("Request for Quotation", "Purchase Invoice"): [
		{
			"type": "chain",
			"via": ("Request for Quotation", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Invoice"),
		}
	],
	("Supplier Quotation", "Purchase Invoice"): [
		{
			"type": "chain",
			"via": ("Supplier Quotation", "Purchase Order"),
			"then": ("Purchase Order", "Purchase Invoice"),
		}
	],
	("Purchase Receipt", "Payment Entry"): [
		{
			"type": "chain",
			"via": ("Purchase Receipt", "Purchase Invoice"),
			"then": ("Purchase Invoice", "Payment Entry"),
		}
	],
	("Material Request", "Payment Entry"): [
		{
			"type": "chain",
			"via": ("Material Request", "Purchase Invoice"),
			"then": ("Purchase Invoice", "Payment Entry"),
		}
	],
	("Request for Quotation", "Payment Entry"): [
		{
			"type": "chain",
			"via": ("Request for Quotation", "Purchase Invoice"),
			"then": ("Purchase Invoice", "Payment Entry"),
		}
	],
	("Supplier Quotation", "Payment Entry"): [
		{
			"type": "chain",
			"via": ("Supplier Quotation", "Purchase Invoice"),
			"then": ("Purchase Invoice", "Payment Entry"),
		}
	],
	("Lead", "Sales Order"): [
		{"type": "chain", "via": ("Lead", "Quotation"), "then": ("Quotation", "Sales Order")}
	],
	("Opportunity", "Sales Order"): [
		{"type": "chain", "via": ("Opportunity", "Quotation"), "then": ("Quotation", "Sales Order")}
	],
}


def get_linked_documents(source_doctype, source_name, target_doctype):
	"""Return distinct linked document names for target_doctype from source document."""
	if source_doctype == target_doctype and source_name:
		return [source_name]

	resolvers = LINK_RESOLVERS.get((source_doctype, target_doctype), [])
	names = set()

	for rule in resolvers:
		names.update(_resolve_rule(rule, source_doctype, source_name))

	return _filter_readable(sorted(names), target_doctype)


def _resolve_rule(rule, source_doctype, source_name):
	rule_type = rule.get("type")

	if rule_type == "chain":
		intermediate = get_linked_documents(source_doctype, source_name, rule["via"][1])
		results = set()
		for docname in intermediate:
			results.update(
				get_linked_documents(rule["then"][0], docname, rule["then"][1])
			)
		return results

	if rule_type == "field":
		filters = {rule["field"]: source_name, **(rule.get("filters") or {})}
		field = rule.get("return_field") or "name"
		return frappe.get_all(rule["doctype"], filters=filters, pluck=field, distinct=True)

	if rule_type == "self_field":
		doc = frappe.get_doc(source_doctype, source_name)
		for key, value in (rule.get("filters") or {}).items():
			if doc.get(key) != value:
				return []
		field_value = doc.get(rule["field"])
		return [field_value] if field_value else []

	if rule_type == "child_rows":
		filters = {"parent": source_name, **(rule.get("filters") or {})}
		values = frappe.get_all(
			rule["child_doctype"], filters=filters, pluck=rule["field"], distinct=True
		)
		return [value for value in values if value]

	if rule_type in ("child", "direct_child"):
		filters = {rule["link_field"]: source_name, **(rule.get("filters") or {})}
		if rule.get("return_field"):
			return frappe.get_all(
				rule["child_doctype"], filters=filters, pluck=rule["return_field"], distinct=True
			)

		parents = frappe.get_all(
			rule["child_doctype"], filters=filters, pluck="parent", distinct=True
		)
		parent_doctype = rule["parent_doctype"]
		return [name for name in parents if frappe.db.exists(parent_doctype, name)]

	return set()


def _filter_readable(names, doctype):
	if not names:
		return []
	if not frappe.has_permission(doctype, "read"):
		return []
	return names
