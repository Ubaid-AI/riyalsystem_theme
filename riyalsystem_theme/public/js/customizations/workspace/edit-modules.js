/*
 * Edit Modules dialog enhancements (Phase 3)
 * Adds hide from menu, open dashboard, and dashboard link fields.
 */
(function () {
	'use strict';

	function get_side_menu_vm() {
		const el = document.getElementById('side-menu-component');
		if (!el) {
			return null;
		}

		if (el.__vue_app__) {
			const app = el.__vue_app__;
			if (app._instance && app._instance.proxy) {
				return app._instance.proxy;
			}
		}

		if (el.__vue__) {
			return el.__vue__;
		}

		return null;
	}

	function cint(value) {
		return parseInt(value, 10) || 0;
	}

	function patch_edit_modules_dialog(vm) {
		if (!vm || vm._dv_edit_modules_patched || typeof vm.open_edit_modules_dialog !== 'function') {
			return !!vm && vm._dv_edit_modules_patched;
		}

		const original_open_dialog = vm.open_edit_modules_dialog.bind(vm);

		vm.open_edit_modules_dialog = function () {
			if (!vm.modules_list || !vm.modules_list.length) {
				return original_open_dialog();
			}

			const rows = vm.modules_list.map(function (mod, index) {
				const icon =
					mod.icon && mod.icon.length
						? mod.icon
						: vm.module_icon && vm.module_icon[mod.name]
							? vm.module_icon[mod.name]
							: 'fal fa-folder';

				return {
					title: mod.custom_menu_title || mod.title || mod.name,
					name: mod.name,
					icon: icon.startsWith('fal') ? icon : vm.module_icon[mod.name] || 'fal fa-folder',
					custom_hide_from_menu: cint(mod.custom_hide_from_menu),
					custom_open_dashboard: cint(mod.custom_open_dashboard),
					custom_default_dashboard: mod.custom_default_dashboard || '',
					parent_page: mod.parent_page || '',
					sequence_id: cint(mod.sequence_id) || index + 1,
					sequence: cint(mod.sequence_id) || index + 1,
				};
			});

			vm.edit_module_dialog = new frappe.ui.Dialog({
				title: __('Edit Modules'),
				primary_action_label: __('Save'),
				fields: [
					{
						fieldname: 'modules',
						fieldtype: 'Table',
						label: __('Modules list'),
						editable_grid: 0,
						data: rows,
						get_data: function () {
							return rows;
						},
						fields: [
							{
								fieldname: 'sequence_id',
								fieldtype: 'Int',
								label: __('Sequence'),
								in_list_view: 1,
								columns: 1,
								default: 1,
							},
							{
								fieldname: 'name',
								fieldtype: 'Data',
								label: __('Module Name'),
								in_list_view: 0,
								read_only: 1,
							},
							{ fieldtype: 'Column Break' },
							{
								fieldname: 'title',
								fieldtype: 'Data',
								label: __('Menu Title'),
								in_list_view: 1,
								reqd: 1,
							},
							{
								fieldname: 'parent_page',
								fieldtype: 'Link',
								options: 'Workspace',
								label: __('Parent Group'),
								in_list_view: 1,
							},
							{
								fieldname: 'icon',
								fieldtype: 'Icon',
								label: __('Icon'),
								in_list_view: 1,
								default: 'fal fa-folder',
							},
							{ fieldtype: 'Column Break' },
							{
								fieldname: 'custom_hide_from_menu',
								fieldtype: 'Check',
								label: __('Hide From Menu'),
								in_list_view: 1,
								columns: 2,
							},
							{
								fieldname: 'custom_open_dashboard',
								fieldtype: 'Check',
								label: __('Open Dashboard'),
								in_list_view: 1,
								columns: 2,
							},
							{
								fieldname: 'custom_default_dashboard',
								fieldtype: 'Link',
								options: 'Dashboard',
								label: __('Default Dashboard'),
								in_list_view: 1,
								depends_on: 'eval:doc.custom_open_dashboard==1',
								mandatory_depends_on: 'eval:doc.custom_open_dashboard==1',
							},
						],
					},
				],
				primary_action: function ({ modules }) {
					const payload = [];
					const new_rows = modules.filter(function (row) {
						return row.__islocal;
					});

					vm.modules_list.forEach(function (mod) {
						const row = modules.find(function (item) {
							return item.name === mod.name;
						});

						payload.push({
							idx: row && row.idx ? row.idx : 0,
							sequence_id: cint(row && row.sequence_id) || (row && row.idx ? row.idx : 0),
							name: row && row.name ? row.name : mod.name,
							title: row && row.title ? row.title : mod.title || mod.name,
							label: row && row.title ? row.title : mod.label || mod.name,
							icon: row && row.icon ? row.icon : mod.icon,
							parent_page: row && row.parent_page ? row.parent_page : '',
							custom_hide_from_menu: cint(row && row.custom_hide_from_menu),
							custom_open_dashboard: cint(row && row.custom_open_dashboard),
							custom_default_dashboard:
								row && row.custom_default_dashboard ? row.custom_default_dashboard : '',
							_is_deleted: row && row.name && !row.__islocal ? 'false' : 'true',
							_is_new: 'false',
						});
					});

					new_rows.forEach(function (row) {
						payload.push({
							idx: row.idx,
							sequence_id: cint(row.sequence_id) || row.idx,
							name: row.title,
							title: row.title,
							label: row.title,
							icon: row.icon || 'fal fa-folder',
							parent_page: row.parent_page || '',
							custom_hide_from_menu: cint(row.custom_hide_from_menu),
							custom_open_dashboard: cint(row.custom_open_dashboard),
							custom_default_dashboard: row.custom_default_dashboard || '',
							content: JSON.stringify([
								{
									type: 'header',
									data: { text: row.title },
								},
							]),
							_is_deleted: 'false',
							_is_new: 'true',
						});
					});

					const updated_rows = payload.filter(function (row) {
						return row._is_new === 'false' && row._is_deleted === 'false';
					});
					const deleted_rows = payload.filter(function (row) {
						return row._is_deleted === 'true';
					});
					const added_rows = payload.filter(function (row) {
						return row._is_new === 'true';
					});

					frappe.confirm(
						`
						<div class="alert alert-warning">
							<h4><i class="far fa-info-circle mr-1"></i> ${__(
								'Are you sure you want to update ({0}) modules?',
								[updated_rows.length]
							)}</h4>
							<div>${__('<b>Deleted Modules : </b> ( {0} )', [
								deleted_rows.map(function (row) {
									return row.title;
								}).join(', '),
							])}</div>
							<div class="mt-2">${__('<b>New Modules : </b> ( {0} )', [
								added_rows.map(function (row) {
									return row.title;
								}).join(', '),
							])}</div>
						</div>
						`,
						function () {
							frappe.call({
								type: 'POST',
								method: 'riyalsystem_theme.api.update_menu_modules',
								args: { modules: payload },
								callback: function () {
									vm.edit_module_dialog.hide();
									frappe.show_alert({
										message: __('Menu updated successfully'),
										indicator: 'green',
									});
									frappe.ui.toolbar.clear_cache();
								},
							});
						}
					);
				},
				secondary_action_label: __('Cancel'),
				secondary_action: function () {},
			});

			if (
				vm.edit_module_dialog.fields_dict.modules.grid.grid_buttons &&
				vm.edit_module_dialog.fields_dict.modules.grid.grid_buttons.find('.grid-remove-all-rows').length
			) {
				vm.edit_module_dialog.fields_dict.modules.grid.grid_buttons
					.find('.grid-remove-all-rows')
					.hide();
			}

			vm.edit_module_dialog.show();
		};

		vm._dv_edit_modules_patched = true;
		return true;
	}

	function ensure_patch() {
		if (patch_edit_modules_dialog(get_side_menu_vm())) {
			return;
		}

		if (frappe._dv_edit_modules_patch_timer) {
			return;
		}

		let attempts = 0;
		frappe._dv_edit_modules_patch_timer = setInterval(function () {
			attempts += 1;
			if (patch_edit_modules_dialog(get_side_menu_vm()) || attempts > 50) {
				clearInterval(frappe._dv_edit_modules_patch_timer);
				frappe._dv_edit_modules_patch_timer = null;
			}
		}, 200);
	}

	$(document).one('app-loaded', ensure_patch);
})();
