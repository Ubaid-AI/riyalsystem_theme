"""Document flow definitions for the visual process tracker."""

from frappe import _

# Each flow is a linear sequence of steps. Steps can define:
# - make_methods: {source_doctype: method_path} for document creation
# - create_action: optional override ("payment_entry", "trigger")
# - trigger: form trigger name when create_action is "trigger"

DOCUMENT_FLOWS = {
	"selling": {
		"label": _("Selling"),
		"steps": [
			{"doctype": "Quotation", "label": _("Quotation")},
			{
				"doctype": "Sales Order",
				"label": _("Sales Order"),
				"make_methods": {
					"Quotation": "erpnext.selling.doctype.quotation.quotation.make_sales_order",
				},
			},
			{
				"doctype": "Delivery Note",
				"label": _("Delivery Note"),
				"make_methods": {
					"Sales Order": "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note",
				},
			},
			{
				"doctype": "Sales Invoice",
				"label": _("Sales Invoice"),
				"make_methods": {
					"Sales Order": "erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice",
					"Delivery Note": "erpnext.stock.doctype.delivery_note.delivery_note.make_sales_invoice",
				},
			},
			{
				"doctype": "Payment Entry",
				"label": _("Payment Entry"),
				"create_action": "payment_entry",
				"make_methods": {
					"Sales Invoice": "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry",
					"Sales Order": "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry",
				},
			},
		],
	},
	"buying": {
		"label": _("Buying"),
		"steps": [
			{"doctype": "Material Request", "label": _("Material Request")},
			{
				"doctype": "Request for Quotation",
				"label": _("Request for Quotation"),
				"make_methods": {
					"Material Request": "erpnext.stock.doctype.material_request.material_request.make_request_for_quotation",
				},
			},
			{
				"doctype": "Supplier Quotation",
				"label": _("Supplier Quotation"),
				"create_action": "trigger",
				"trigger": "make_supplier_quotation",
				"make_methods": {
					"Request for Quotation": "erpnext.buying.doctype.request_for_quotation.request_for_quotation.make_supplier_quotation_from_rfq",
				},
			},
			{
				"doctype": "Purchase Order",
				"label": _("Purchase Order"),
				"make_methods": {
					"Supplier Quotation": "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
					"Material Request": "erpnext.stock.doctype.material_request.material_request.make_purchase_order",
				},
			},
			{
				"doctype": "Purchase Receipt",
				"label": _("Purchase Receipt"),
				"make_methods": {
					"Purchase Order": "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt",
				},
			},
			{
				"doctype": "Purchase Invoice",
				"label": _("Purchase Invoice"),
				"make_methods": {
					"Purchase Order": "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice",
					"Purchase Receipt": "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
				},
			},
			{
				"doctype": "Payment Entry",
				"label": _("Payment Entry"),
				"create_action": "payment_entry",
				"make_methods": {
					"Purchase Invoice": "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry",
					"Purchase Order": "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry",
				},
			},
		],
	},
	"crm": {
		"label": _("CRM"),
		"steps": [
			{"doctype": "Lead", "label": _("Lead")},
			{
				"doctype": "Opportunity",
				"label": _("Opportunity"),
				"make_methods": {
					"Lead": "erpnext.crm.doctype.lead.lead.make_opportunity",
				},
			},
			{
				"doctype": "Quotation",
				"label": _("Quotation"),
				"make_methods": {
					"Lead": "erpnext.crm.doctype.lead.lead.make_quotation",
					"Opportunity": "erpnext.crm.doctype.opportunity.opportunity.make_quotation",
				},
			},
			{
				"doctype": "Sales Order",
				"label": _("Sales Order"),
				"make_methods": {
					"Quotation": "erpnext.selling.doctype.quotation.quotation.make_sales_order",
				},
			},
		],
	},
}


def get_flow_for_doctype(doctype, doc=None):
	"""Return (flow_id, flow, step_index) for a doctype, or None."""
	candidates = []
	for flow_id, flow in DOCUMENT_FLOWS.items():
		for idx, step in enumerate(flow["steps"]):
			if step["doctype"] == doctype:
				candidates.append((flow_id, flow, idx))

	if not candidates:
		return None

	if len(candidates) == 1:
		return candidates[0]

	return _pick_flow(candidates, doctype, doc)


def _pick_flow(candidates, doctype, doc):
	"""Choose the best flow when a doctype appears in multiple flows."""
	import frappe

	if doctype == "Payment Entry" and doc:
		ref_doctypes = frappe.get_all(
			"Payment Entry Reference",
			filters={"parent": doc.name},
			pluck="reference_doctype",
		)
		buying_refs = {"Purchase Invoice", "Purchase Order"}
		if buying_refs.intersection(set(ref_doctypes)):
			for candidate in candidates:
				if candidate[0] == "buying":
					return candidate

		for candidate in candidates:
			if candidate[0] == "selling":
				return candidate

	if doctype in ("Quotation", "Sales Order"):
		for candidate in candidates:
			if candidate[0] == "selling":
				return candidate

	return candidates[0]


def get_all_flow_doctypes():
	return {step["doctype"] for flow in DOCUMENT_FLOWS.values() for step in flow["steps"]}
