/**
 * Visual Document Flow / Process Tracker for ERPNext transactional forms.
 * Renders a horizontal stepper below the form title and above tabs.
 */
frappe.provide("riyalsystem_theme.document_flow");

riyalsystem_theme.document_flow = {
	FLOW_DOCTYPES: new Set([
		"Quotation",
		"Sales Order",
		"Delivery Note",
		"Sales Invoice",
		"Payment Entry",
		"Material Request",
		"Request for Quotation",
		"Supplier Quotation",
		"Purchase Order",
		"Purchase Receipt",
		"Purchase Invoice",
		"Lead",
		"Opportunity",
	]),

	init() {
		if (this._initialized) return;
		this._initialized = true;

		$(document).on("form-refresh", (e, frm) => {
			this.on_form_refresh(frm);
		});
	},

	on_form_refresh(frm) {
		if (!frm || !this.FLOW_DOCTYPES.has(frm.doctype)) {
			this.remove_tracker(frm);
			return;
		}

		this.load_and_render(frm);
	},

	remove_tracker(frm) {
		if (frm?._document_flow_wrapper) {
			frm._document_flow_wrapper.remove();
			frm._document_flow_wrapper = null;
		}
		if (frm?._document_flow_picker) {
			frm._document_flow_picker = null;
		}
	},

	get_mount_point(frm) {
		const $layout = frm.layout?.wrapper;
		if (!$layout) return null;

		const $tabs = $layout.find(".form-tabs-list").first();
		if ($tabs.length) {
			return $tabs;
		}
		return $layout;
	},

	load_and_render(frm) {
		const args = {
			doctype: frm.doctype,
			is_new: frm.is_new() ? 1 : 0,
		};

		if (!frm.is_new()) {
			args.name = frm.doc.name;
		}

		frappe.call({
			method: "riyalsystem_theme.document_flow.document_flow.get_document_flow",
			args,
			callback: (r) => {
				if (!r.message?.steps?.length) {
					this.remove_tracker(frm);
					return;
				}
				this.render(frm, r.message);
			},
		});
	},

	render(frm, data) {
		this.remove_tracker(frm);

		const $mount = this.get_mount_point(frm);
		if (!$mount) return;

		const $wrapper = $(`
			<div class="rst-document-flow${
				data.is_unsaved ? " rst-document-flow--unsaved" : ""
			}" role="navigation" aria-label="${__("Document Flow")}">
				<div class="rst-document-flow__header">
					<span class="rst-document-flow__title">${data.flow_label}</span>
					${
						data.is_unsaved
							? `<span class="rst-document-flow__unsaved-tag">${__("Unsaved")}</span>`
							: ""
					}
				</div>
				<div class="rst-document-flow__track"></div>
			</div>
		`);

		const $track = $wrapper.find(".rst-document-flow__track");

		data.steps.forEach((step, index) => {
			if (index > 0) {
				$track.append(this.build_arrow(step, data.steps[index - 1]));
			}
			$track.append(this.build_step(step, frm, data));
		});

		$mount.before($wrapper);
		frm._document_flow_wrapper = $wrapper;
	},

	build_arrow(step, prev_step) {
		const is_active =
			prev_step.status === "completed" ||
			prev_step.status === "current" ||
			(step.status !== "pending" && step.status !== "draft");

		return $(`
			<div class="rst-document-flow__arrow${
				is_active ? " rst-document-flow__arrow--active" : ""
			}" aria-hidden="true">
				<svg viewBox="0 0 24 24" width="20" height="20" focusable="false">
					<path fill="currentColor" d="M4 11h12.17l-4.88-4.88L13 4.5 20.5 12 13 19.5l-1.71-1.71L16.17 13H4v-2z"/>
				</svg>
			</div>
		`);
	},

	build_step(step, frm, data) {
		const status = step.status;
		const count = step.count || 0;
		const show_count = count > 1 && !step.is_current;
		const is_clickable = step.is_navigable || step.can_create;
		const label = this.get_step_label(step);

		const $step = $(`
			<div
				class="rst-document-flow__step rst-document-flow__step--${status}${
				is_clickable ? " rst-document-flow__step--clickable" : ""
			}"
				data-doctype="${frappe.utils.escape_html(step.doctype)}"
				title="${frappe.utils.escape_html(this.get_step_title(step))}"
			>
				<div class="rst-document-flow__icon">${this.get_step_icon(step)}</div>
				<div class="rst-document-flow__label">${frappe.utils.escape_html(label)}</div>
				${
					show_count
						? `<span class="rst-document-flow__badge" aria-label="${__(
								"{0} linked documents",
								[count]
						  )}">${count}</span>`
						: ""
				}
			</div>
		`);

		if (is_clickable) {
			$step.on("click", (e) => {
				e.stopPropagation();
				this.on_step_click(step, frm, $step);
			});
		}

		return $step;
	},

	get_step_label(step) {
		if (step.status === "draft") {
			return __("Draft {0}", [__(step.label)]);
		}

		const label = __(step.label);
		if (step.count > 1 && !step.is_current) {
			return `${label} (${step.count})`;
		}
		return label;
	},

	get_step_title(step) {
		if (step.status === "draft") {
			return __("This document has not been saved yet");
		}
		if (step.is_navigable && step.count > 1) {
			return __("Click to choose from {0} linked documents", [step.count]);
		}
		if (step.is_navigable) {
			return __("Click to open linked document");
		}
		if (step.can_create) {
			return __("Click to create {0}", [__(step.label)]);
		}
		if (step.is_current) {
			return __("You are here");
		}
		return __(step.label);
	},

	get_step_icon(step) {
		if (step.status === "draft") {
			return '<span class="rst-document-flow__draft-icon"><i class="fa fa-pencil-alt"></i></span>';
		}
		if (step.status === "completed" || step.status === "current") {
			return '<span class="rst-document-flow__check">✓</span>';
		}
		return '<span class="rst-document-flow__dot"></span>';
	},

	on_step_click(step, frm, $step) {
		if (step.is_navigable) {
			this.open_linked_documents(step, $step);
			return;
		}

		if (step.can_create) {
			this.create_document(step, frm);
		}
	},

	open_linked_documents(step, $step) {
		const { doctype, names } = step;

		if (names.length === 1) {
			frappe.set_route("Form", doctype, names[0]);
			return;
		}

		this.show_document_picker(step, $step);
	},

	show_document_picker(step, $anchor) {
		this.hide_document_picker();

		const $picker = $(`
			<div class="rst-document-flow__picker">
				<div class="rst-document-flow__picker-header">
					<span>${frappe.utils.escape_html(__(step.label))}</span>
					<span class="rst-document-flow__picker-count">${step.count}</span>
				</div>
				<div class="rst-document-flow__picker-list"></div>
			</div>
		`);

		const $list = $picker.find(".rst-document-flow__picker-list");

		step.names.forEach((name) => {
			const $item = $(`
				<button type="button" class="rst-document-flow__picker-item">
					<span class="rst-document-flow__picker-name">${frappe.utils.escape_html(name)}</span>
					<i class="fa fa-external-link-alt"></i>
				</button>
			`);

			$item.on("click", (e) => {
				e.stopPropagation();
				this.hide_document_picker();
				frappe.set_route("Form", step.doctype, name);
			});

			$list.append($item);
		});

		$("body").append($picker);

		const offset = $anchor.offset();
		const picker_width = $picker.outerWidth();
		const left = Math.max(
			8,
			Math.min(
				offset.left + $anchor.outerWidth() / 2 - picker_width / 2,
				$(window).width() - picker_width - 8
			)
		);

		$picker.css({
			top: offset.top + $anchor.outerHeight() + 8,
			left,
		});

		this._active_picker = $picker;

		setTimeout(() => {
			$(document).on("click.rst-document-flow-picker", () => this.hide_document_picker());
		}, 0);
	},

	hide_document_picker() {
		if (this._active_picker) {
			this._active_picker.remove();
			this._active_picker = null;
		}
		$(document).off("click.rst-document-flow-picker");
	},

	create_document(step, frm) {
		if (step.create_action === "trigger" && step.trigger) {
			frm.trigger(step.trigger);
			return;
		}

		if (step.create_action === "payment_entry") {
			this.create_payment_entry(frm);
			return;
		}

		if (step.make_method) {
			frappe.model.open_mapped_doc({
				method: step.make_method,
				frm: frm,
			});
		}
	},

	create_payment_entry(frm) {
		let method = "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry";
		if (frm.doc.__onload?.make_payment_via_journal_entry) {
			if (["Sales Invoice", "Purchase Invoice"].includes(frm.doctype)) {
				method =
					"erpnext.accounts.doctype.journal_entry.journal_entry.get_payment_entry_against_invoice";
			} else {
				method =
					"erpnext.accounts.doctype.journal_entry.journal_entry.get_payment_entry_against_order";
			}
		}

		frappe.call({
			method: method,
			args: { dt: frm.doc.doctype, dn: frm.doc.name },
			callback(r) {
				if (r.message) {
					const doclist = frappe.model.sync(r.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
				}
			},
		});
	},
};

riyalsystem_theme.document_flow.init();
