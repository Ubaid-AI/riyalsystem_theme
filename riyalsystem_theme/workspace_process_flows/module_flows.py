"""Multi-section workspace process flow definitions.

Selling and Buying use a single linear track. Other modules use multiple
process rows to reflect real ERPNext workflows and document relationships.
"""

PROCESS_FLOWS = {
	"selling": {
		"block_name": "RST Selling Process Flow",
		"title": "Sales Cycle",
		"subtitle": "Quotation through payment — click any step to create a new document.",
		"workspace": "Selling",
		"steps": [
			{"doctype": "Quotation", "label": "Quotation", "icon": "document"},
			{"doctype": "Sales Order", "label": "Sales Order", "icon": "cart"},
			{"doctype": "Delivery Note", "label": "Delivery Note", "icon": "truck"},
			{"doctype": "Sales Invoice", "label": "Sales Invoice", "icon": "invoice"},
			{"doctype": "Payment Entry", "label": "Payment Entry", "icon": "payment"},
		],
	},
	"buying": {
		"block_name": "RST Buying Process Flow",
		"title": "Procurement Cycle",
		"subtitle": "Request materials through supplier payment — click any step to create a new document.",
		"workspace": "Buying",
		"steps": [
			{"doctype": "Material Request", "label": "Material Request", "icon": "material"},
			{"doctype": "Request for Quotation", "label": "Request for Quotation", "icon": "rfq"},
			{"doctype": "Supplier Quotation", "label": "Supplier Quotation", "icon": "supplier"},
			{"doctype": "Purchase Order", "label": "Purchase Order", "icon": "purchase"},
			{"doctype": "Purchase Receipt", "label": "Purchase Receipt", "icon": "receipt"},
			{"doctype": "Purchase Invoice", "label": "Purchase Invoice", "icon": "invoice"},
			{"doctype": "Payment Entry", "label": "Payment Entry", "icon": "payment"},
		],
	},
	"crm": {
		"block_name": "RST CRM Process Flow",
		"title": "CRM Workflows",
		"subtitle": "Lead capture, opportunity management, and customer conversion — click any step to create a new document.",
		"workspace": "CRM",
		"flows": [
			{
				"title": "Lead Management",
				"description": "Capture inbound interest, qualify leads, and schedule follow-ups before conversion.",
				"steps": [
					{"doctype": "Lead", "label": "Lead", "icon": "lead"},
					{"doctype": "Opportunity", "label": "Opportunity", "icon": "opportunity"},
					{"doctype": "Communication", "label": "Communication", "icon": "communication"},
				],
			},
			{
				"title": "Opportunity Management",
				"description": "Track deals through stages, prepare proposals, and link to campaigns or prospects.",
				"steps": [
					{"doctype": "Prospect", "label": "Prospect", "icon": "prospect"},
					{"doctype": "Opportunity", "label": "Opportunity", "icon": "opportunity"},
					{"doctype": "Quotation", "label": "Quotation", "icon": "document"},
					{"doctype": "Campaign", "label": "Campaign", "icon": "campaign"},
				],
			},
			{
				"title": "Customer Conversion",
				"description": "Convert won opportunities into customers and start the sales order cycle.",
				"steps": [
					{"doctype": "Customer", "label": "Customer", "icon": "customer"},
					{"doctype": "Quotation", "label": "Quotation", "icon": "document"},
					{"doctype": "Sales Order", "label": "Sales Order", "icon": "cart"},
					{"doctype": "Contract", "label": "Contract", "icon": "contract"},
				],
			},
		],
	},
	"stock": {
		"block_name": "RST Stock Process Flow",
		"title": "Inventory Workflows",
		"subtitle": "Inbound, internal movement, outbound, and stock control — click any step to create a new document.",
		"workspace": "Stock",
		"flows": [
			{
				"title": "Inbound Inventory",
				"description": "Receive purchased or transferred stock into warehouses via purchase or stock entry.",
				"steps": [
					{"doctype": "Purchase Order", "label": "Purchase Order", "icon": "purchase"},
					{"doctype": "Purchase Receipt", "label": "Purchase Receipt", "icon": "receipt"},
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
				],
			},
			{
				"title": "Internal Transfers",
				"description": "Move material between warehouses, repack, or fulfill internal material requests.",
				"steps": [
					{"doctype": "Material Request", "label": "Material Request", "icon": "material"},
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
					{"doctype": "Pick List", "label": "Pick List", "icon": "pick"},
				],
			},
			{
				"title": "Outbound Inventory",
				"description": "Pick, pack, and ship items against sales orders or delivery requirements.",
				"steps": [
					{"doctype": "Sales Order", "label": "Sales Order", "icon": "cart"},
					{"doctype": "Pick List", "label": "Pick List", "icon": "pick"},
					{"doctype": "Delivery Note", "label": "Delivery Note", "icon": "truck"},
					{"doctype": "Sales Invoice", "label": "Sales Invoice", "icon": "invoice"},
				],
			},
			{
				"title": "Stock Reconciliation",
				"description": "Adjust on-hand quantities after physical counts or inventory audits.",
				"steps": [
					{"doctype": "Stock Reconciliation", "label": "Stock Reconciliation", "icon": "reconciliation"},
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
				],
			},
		],
	},
	"manufacturing": {
		"block_name": "RST Manufacturing Process Flow",
		"title": "Manufacturing Workflows",
		"subtitle": "Plan production, execute work orders, procure materials, and finish goods — click any step to create a new document.",
		"workspace": "Manufacturing",
		"flows": [
			{
				"title": "Production Planning",
				"description": "Define BOMs, plan demand from sales orders or material requests, and create work orders.",
				"steps": [
					{"doctype": "BOM", "label": "BOM", "icon": "bom"},
					{"doctype": "Production Plan", "label": "Production Plan", "icon": "production_plan"},
					{"doctype": "Work Order", "label": "Work Order", "icon": "work_order"},
				],
			},
			{
				"title": "Manufacturing Execution",
				"description": "Issue raw materials, record operations on the shop floor, and track job cards.",
				"steps": [
					{"doctype": "Work Order", "label": "Work Order", "icon": "work_order"},
					{"doctype": "Job Card", "label": "Job Card", "icon": "job_card"},
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
				],
			},
			{
				"title": "Material Procurement",
				"description": "Raise material requests and purchase orders when BOM components are not in stock.",
				"steps": [
					{"doctype": "Material Request", "label": "Material Request", "icon": "material"},
					{"doctype": "Purchase Order", "label": "Purchase Order", "icon": "purchase"},
					{"doctype": "Purchase Receipt", "label": "Purchase Receipt", "icon": "receipt"},
				],
			},
			{
				"title": "Finished Goods Production",
				"description": "Manufacture finished items and move them to stock for sales or transfer.",
				"steps": [
					{"doctype": "Work Order", "label": "Work Order", "icon": "work_order"},
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
					{"doctype": "Delivery Note", "label": "Delivery Note", "icon": "truck"},
				],
			},
		],
	},
	"accounting": {
		"block_name": "RST Accounting Process Flow",
		"title": "Accounting Workflows",
		"subtitle": "Collections, payments, bank reconciliation, journals, and period closing — click any step to create a new document.",
		"workspace": "Accounting",
		"flows": [
			{
				"title": "Customer Collections",
				"description": "Bill customers, send payment reminders, and record incoming receipts.",
				"steps": [
					{"doctype": "Sales Invoice", "label": "Sales Invoice", "icon": "invoice"},
					{"doctype": "Dunning", "label": "Dunning", "icon": "dunning"},
					{"doctype": "Payment Entry", "label": "Payment Entry", "icon": "payment"},
				],
			},
			{
				"title": "Supplier Payments",
				"description": "Record supplier bills and pay outstanding purchase invoices.",
				"steps": [
					{"doctype": "Purchase Invoice", "label": "Purchase Invoice", "icon": "receipt"},
					{"doctype": "Payment Entry", "label": "Payment Entry", "icon": "payment"},
					{"doctype": "Journal Entry", "label": "Journal Entry", "icon": "journal"},
				],
			},
			{
				"title": "Bank Reconciliation",
				"description": "Import bank transactions and match them against payment entries and invoices.",
				"steps": [
					{"doctype": "Bank Transaction", "label": "Bank Transaction", "icon": "bank"},
					{"doctype": "Payment Reconciliation", "label": "Payment Reconciliation", "icon": "reconciliation"},
					{"doctype": "Payment Entry", "label": "Payment Entry", "icon": "payment"},
				],
			},
			{
				"title": "Journal Entries",
				"description": "Post manual adjustments, accruals, and opening balances to the general ledger.",
				"steps": [
					{"doctype": "Journal Entry", "label": "Journal Entry", "icon": "journal"},
					{"doctype": "Journal Entry Template", "label": "JE Template", "icon": "document"},
				],
			},
			{
				"title": "Period Closing Activities",
				"description": "Close accounting periods and freeze prior transactions after review.",
				"steps": [
					{"doctype": "Process Period Closing Voucher", "label": "Process Closing", "icon": "closing"},
					{"doctype": "Period Closing Voucher", "label": "Period Closing", "icon": "closing"},
				],
			},
		],
	},
	"projects": {
		"block_name": "RST Projects Process Flow",
		"title": "Project Workflows",
		"subtitle": "Plan, execute, track time, and bill project work — click any step to create a new document.",
		"workspace": "Projects",
		"flows": [
			{
				"title": "Project Setup",
				"description": "Create projects from templates, define tasks, and assign team members.",
				"steps": [
					{"doctype": "Project Template", "label": "Project Template", "icon": "project"},
					{"doctype": "Project", "label": "Project", "icon": "project"},
					{"doctype": "Task", "label": "Task", "icon": "task"},
				],
			},
			{
				"title": "Execution & Tracking",
				"description": "Log timesheets, update progress, and track costs against the project budget.",
				"steps": [
					{"doctype": "Task", "label": "Task", "icon": "task"},
					{"doctype": "Timesheet", "label": "Timesheet", "icon": "timesheet"},
					{"doctype": "Project Update", "label": "Project Update", "icon": "document"},
				],
			},
			{
				"title": "Project Billing",
				"description": "Invoice billable time and expenses to the customer linked to the project.",
				"steps": [
					{"doctype": "Timesheet", "label": "Timesheet", "icon": "timesheet"},
					{"doctype": "Sales Invoice", "label": "Sales Invoice", "icon": "invoice"},
					{"doctype": "Payment Entry", "label": "Payment Entry", "icon": "payment"},
				],
			},
		],
	},
	"hr": {
		"block_name": "RST HR Process Flow",
		"title": "HR Workflows",
		"subtitle": "Recruitment, employee lifecycle, attendance, and payroll — click any step to create a new document.",
		"workspace": "HR",
		"footer": "Recruitment, attendance, leave, and payroll documents require the HRMS app.",
		"flows": [
			{
				"title": "Recruitment Process",
				"description": "Publish openings, screen applicants, conduct interviews, and extend offers.",
				"steps": [
					{"doctype": "Job Opening", "label": "Job Opening", "icon": "job_opening"},
					{"doctype": "Job Applicant", "label": "Job Applicant", "icon": "applicant"},
					{"doctype": "Interview", "label": "Interview", "icon": "interview"},
					{"doctype": "Job Offer", "label": "Job Offer", "icon": "job_offer"},
				],
			},
			{
				"title": "Employee Lifecycle",
				"description": "Onboard new hires, maintain employee records, and manage separations.",
				"steps": [
					{"doctype": "Employee", "label": "Employee", "icon": "employee"},
					{"doctype": "Employee Onboarding", "label": "Onboarding", "icon": "onboarding"},
					{"doctype": "Employee Separation", "label": "Separation", "icon": "employee"},
				],
			},
			{
				"title": "Attendance & Leave",
				"description": "Track daily attendance, shift assignments, and approved leave applications.",
				"steps": [
					{"doctype": "Shift Type", "label": "Shift Type", "icon": "attendance"},
					{"doctype": "Attendance", "label": "Attendance", "icon": "attendance"},
					{"doctype": "Leave Application", "label": "Leave Application", "icon": "leave"},
				],
			},
			{
				"title": "Payroll Process",
				"description": "Process salary slips in bulk via payroll entry and submit for payment.",
				"steps": [
					{"doctype": "Salary Structure", "label": "Salary Structure", "icon": "salary"},
					{"doctype": "Payroll Entry", "label": "Payroll Entry", "icon": "payroll"},
					{"doctype": "Salary Slip", "label": "Salary Slip", "icon": "salary"},
				],
			},
		],
	},
	"support": {
		"block_name": "RST Support Process Flow",
		"title": "Support Workflows",
		"subtitle": "Service levels, issue resolution, warranty, and maintenance — click any step to create a new document.",
		"workspace": "Support",
		"flows": [
			{
				"title": "Issue Management",
				"description": "Log customer issues, assign agents, and track resolution against SLAs.",
				"steps": [
					{"doctype": "Issue", "label": "Issue", "icon": "issue"},
					{"doctype": "Service Level Agreement", "label": "SLA", "icon": "sla"},
					{"doctype": "Communication", "label": "Communication", "icon": "communication"},
				],
			},
			{
				"title": "Warranty & Claims",
				"description": "Process warranty claims linked to delivered items and serial numbers.",
				"steps": [
					{"doctype": "Warranty Claim", "label": "Warranty Claim", "icon": "warranty"},
					{"doctype": "Delivery Note", "label": "Delivery Note", "icon": "truck"},
					{"doctype": "Maintenance Visit", "label": "Maintenance Visit", "icon": "maintenance"},
				],
			},
			{
				"title": "Preventive Maintenance",
				"description": "Schedule recurring maintenance visits and track equipment service history.",
				"steps": [
					{"doctype": "Maintenance Schedule", "label": "Maint. Schedule", "icon": "maintenance"},
					{"doctype": "Maintenance Visit", "label": "Maintenance Visit", "icon": "maintenance"},
					{"doctype": "Issue", "label": "Follow-up Issue", "icon": "issue"},
				],
			},
		],
	},
	"quality": {
		"block_name": "RST Quality Process Flow",
		"title": "Quality Workflows",
		"subtitle": "Goals, inspections, actions, and feedback — click any step to create a new document.",
		"workspace": "Quality",
		"flows": [
			{
				"title": "Quality Planning",
				"description": "Define quality goals, procedures, and inspection criteria for items or processes.",
				"steps": [
					{"doctype": "Quality Goal", "label": "Quality Goal", "icon": "quality"},
					{"doctype": "Quality Procedure", "label": "Quality Procedure", "icon": "quality"},
					{"doctype": "Quality Inspection Template", "label": "Inspection Template", "icon": "inspection"},
				],
			},
			{
				"title": "Incoming & In-Process Inspection",
				"description": "Inspect purchased or manufactured items before acceptance or further processing.",
				"steps": [
					{"doctype": "Purchase Receipt", "label": "Purchase Receipt", "icon": "receipt"},
					{"doctype": "Quality Inspection", "label": "Quality Inspection", "icon": "inspection"},
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
				],
			},
			{
				"title": "Corrective Actions & Feedback",
				"description": "Record non-conformances, assign corrective actions, and collect feedback.",
				"steps": [
					{"doctype": "Quality Inspection", "label": "Quality Inspection", "icon": "inspection"},
					{"doctype": "Quality Action", "label": "Quality Action", "icon": "action"},
					{"doctype": "Quality Feedback", "label": "Quality Feedback", "icon": "feedback"},
				],
			},
		],
	},
	"assets": {
		"block_name": "RST Assets Process Flow",
		"title": "Asset Workflows",
		"subtitle": "Acquisition, movement, depreciation, repair, and capitalization — click any step to create a new document.",
		"workspace": "Assets",
		"flows": [
			{
				"title": "Asset Acquisition",
				"description": "Purchase fixed assets via purchase invoice and create asset records.",
				"steps": [
					{"doctype": "Purchase Invoice", "label": "Purchase Invoice", "icon": "receipt"},
					{"doctype": "Asset", "label": "Asset", "icon": "asset"},
					{"doctype": "Asset Category", "label": "Asset Category", "icon": "asset"},
				],
			},
			{
				"title": "Asset Movement & Transfer",
				"description": "Transfer assets between locations, departments, or custodians.",
				"steps": [
					{"doctype": "Asset", "label": "Asset", "icon": "asset"},
					{"doctype": "Asset Movement", "label": "Asset Movement", "icon": "movement"},
					{"doctype": "Location", "label": "Location", "icon": "movement"},
				],
			},
			{
				"title": "Depreciation & Maintenance",
				"description": "Schedule depreciation, record repairs, and maintain asset value over time.",
				"steps": [
					{"doctype": "Asset Depreciation Schedule", "label": "Depreciation", "icon": "depreciation"},
					{"doctype": "Asset Repair", "label": "Asset Repair", "icon": "repair"},
					{"doctype": "Asset Maintenance", "label": "Asset Maintenance", "icon": "maintenance"},
				],
			},
			{
				"title": "Asset Capitalization",
				"description": "Capitalize stock items or composite assets into a single fixed asset.",
				"steps": [
					{"doctype": "Stock Entry", "label": "Stock Entry", "icon": "stock"},
					{"doctype": "Asset Capitalization", "label": "Capitalization", "icon": "asset"},
					{"doctype": "Asset", "label": "Asset", "icon": "asset"},
				],
			},
		],
	},
}
