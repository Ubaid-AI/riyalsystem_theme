from __future__ import unicode_literals
import os, re, json
import frappe
from frappe.utils import flt, cint, get_time, make_filter_tuple, get_filter, add_to_date, cstr, get_timespan_date_range, nowdate, add_days, getdate, add_months, get_datetime
from frappe import _
from frappe.desk.reportview import get_filters_cond
from frappe.cache_manager import clear_user_cache
from six import string_types


@frappe.whitelist()
def get_module_name_from_doctype(doc_name, current_module=""):
    # frappe.msgprint("======"+str(doc_name))
    condition = ""
    if doc_name:
        if current_module:
            condition = "and  w.`name` = {current_module} ".format(current_module=current_module)

        list_od_dicts = frappe.db.sql("""
            select *
                    from (
                            select  w.`name` `module`,
                                 (select restrict_to_domain from `tabModule Def` where `name` = w.module ) restrict_to_domain
                                             from  tabWorkspace w
                                             inner join
                                                        `tabWorkspace Link` l
                                                        on w.`name` = l.parent
                                                         where link_to = '{doc_name}'
                                                          %s
                                )	T
        """.format(doc_name=doc_name), (condition), as_dict=True, debug=False)
        if list_od_dicts:
            return [{"module": list_od_dicts[0]["module"]}]
        else:
            list_od_dicts = frappe.db.sql("""
                select *
                        from (
                                select  w.`name` `module`,
                                     (select restrict_to_domain from `tabModule Def` where `name` = w.module ) restrict_to_domain
                                                 from  tabWorkspace w
                                                 inner join
                                                            `tabWorkspace Link` l
                                                            on w.`name` = l.parent
                                                             where link_to = '{doc_name}'
                                    )	T
            """.format(doc_name=doc_name), as_dict=True, debug=False)
        if list_od_dicts:
            return [{"module": list_od_dicts[0]["module"]}]


@frappe.whitelist()
def change_language(language):
    frappe.db.set_value("User", frappe.session.user, "language", language)
    clear()
    return True


@frappe.whitelist()
def get_current_language():
    return frappe.db.get_value("User", frappe.session.user, "language")


@frappe.whitelist()
def get_company_logo():
    logo_path = ""
    current_company = frappe.defaults.get_user_default("company")
    if current_company:
        logo_path = frappe.db.get_value("Company", current_company, "company_logo")

    return logo_path


@frappe.whitelist(allow_guest=True)
def get_theme_settings():
    slideshow_photos = []
    settings_list = {}
    settings = frappe.db.sql("""
                       SELECT * FROM tabSingles WHERE doctype = 'Theme Settings';
    """, as_dict=True, debug=False)

    for setting in settings:
        settings_list[setting['field']] = setting['value']

    if (("background_type" in settings_list) and settings_list['background_type'] == 'Slideshow'):
        slideshow_photos = frappe.db.sql("""
                               SELECT `photo` FROM `tabSlideshow Photos` WHERE `parent` = 'Theme Settings';
            """, as_dict=True, debug=False)

    def _check(field):
        return cint(settings_list.get(field))

    return {
        'enable_background': settings_list.get('enable_background') or '',
        'background_photo': settings_list.get('background_photo') or '',
        'background_type': settings_list.get('background_type') or '',
        'full_page_background': settings_list.get('full_page_background') or '',
        'transparent_background': settings_list.get('transparent_background') or '',
        'slideshow_photos': slideshow_photos,
        'dark_view': _check('dark_view'),
        'theme_color': settings_list.get('theme_color') or '',
        'open_workspace_on_mobile_menu': _check('open_workspace_on_mobile_menu'),
        'show_icon_label': _check('show_icon_label'),
        'hide_icon_tooltip': _check('hide_icon_tooltip'),
        'always_close_sub_menu': _check('always_close_sub_menu'),
        'menu_opening_type': settings_list.get('menu_opening_type') or '',
        'apply_dark_mode': _check('apply_dark_mode'),
        'apply_on_navbar': _check('apply_on_navbar'),
        'apply_on_menu': _check('apply_on_menu'),
        'apply_on_dashboard': _check('apply_on_dashboard'),
        'apply_on_workspace': _check('apply_on_workspace'),
        'default_type': settings_list.get('default_type') or '',
        'default_workspace': settings_list.get('default_workspace') or '',
        'default_dashboard': settings_list.get('default_dashboard') or '',
        'loading_image': settings_list.get('loading_image') or ''
    }


@frappe.whitelist()
def update_theme_settings(**data):
    data = frappe._dict(data)
    doc = frappe.get_doc("Theme Settings")
    doc.theme_color = data.theme_color or doc.theme_color or "Blue"
    doc.apply_on_menu = cint(data.get("apply_on_menu"))
    doc.apply_on_dashboard = cint(data.get("apply_on_dashboard"))
    doc.apply_on_workspace = cint(data.get("apply_on_workspace"))
    doc.apply_on_navbar = cint(data.get("apply_on_navbar"))
    doc.apply_dark_mode = cint(data.get("apply_dark_mode"))
    doc.dark_view = doc.apply_dark_mode
    doc.save(ignore_permissions=True)
    return doc


@frappe.whitelist()
def get_events(start=getdate(), end=getdate().year, user=None, for_reminder=False, filters=None):
    end = str(getdate().year) + "-12-31"
    if not user:
        user = frappe.session.user

    if isinstance(filters, string_types):
        filters = json.loads(filters)

    filter_condition = get_filters_cond('Event', filters, [])

    tables = ["`tabEvent`"]
    if "`tabEvent Participants`" in filter_condition:
        tables.append("`tabEvent Participants`")

    events = frappe.db.sql("""
        SELECT `tabEvent`.name,
                `tabEvent`.subject,
                `tabEvent`.description,
                `tabEvent`.color,
                `tabEvent`.starts_on,
                `tabEvent`.ends_on,
                `tabEvent`.owner,
                `tabEvent`.all_day,
                `tabEvent`.event_type,
                `tabEvent`.repeat_this_event,
                `tabEvent`.repeat_on,
                `tabEvent`.repeat_till,
                `tabEvent`.monday,
                `tabEvent`.tuesday,
                `tabEvent`.wednesday,
                `tabEvent`.thursday,
                `tabEvent`.friday,
                `tabEvent`.saturday,
                `tabEvent`.sunday
        FROM {tables}
        WHERE (
                (
                    (date(`tabEvent`.starts_on) BETWEEN date(%(start)s) AND date(%(end)s))
                    OR (date(`tabEvent`.ends_on) BETWEEN date(%(start)s) AND date(%(end)s))
                    OR (
                        date(`tabEvent`.starts_on) <= date(%(start)s)
                        AND date(`tabEvent`.ends_on) >= date(%(end)s)
                    )
                )
                OR (
                    date(`tabEvent`.starts_on) <= date(%(start)s)
                    AND `tabEvent`.repeat_this_event=1
                    AND coalesce(`tabEvent`.repeat_till, '3000-01-01') > date(%(start)s)
                )
            )
        {reminder_condition}
        {filter_condition}
        AND (
                `tabEvent`.event_type='Public'
                OR `tabEvent`.owner=%(user)s
                OR EXISTS(
                    SELECT `tabDocShare`.name
                    FROM `tabDocShare`
                    WHERE `tabDocShare`.share_doctype='Event'
                        AND `tabDocShare`.share_name=`tabEvent`.name
                        AND `tabDocShare`.user=%(user)s
                )
            )
        AND `tabEvent`.status='Open'
        ORDER BY `tabEvent`.starts_on""".format(
        tables=", ".join(tables),
        filter_condition=filter_condition,
        reminder_condition="AND coalesce(`tabEvent`.send_reminder, 0)=1" if for_reminder else ""
    ), {
        "start": start,
        "end": end,
        "user": user,
    }, as_dict=1)

    return events


@frappe.whitelist()
def get_doctype_parent_module(doctype=''):
    result = frappe.db.sql(
        """select * from `tabWorkspace Link` where type='Link' and link_to=%s order by idx DESC limit 1""",
        doctype,
        as_dict=True,
    )
    if result and result[0]:
        return result[0].parent


@frappe.whitelist()
def update_menu_modules(modules):
    modules_list = json.loads(modules)
    for module in modules_list:
        if frappe.db.exists("Workspace", module["name"]):
            if (module["_is_deleted"] == 'true'):
                frappe.delete_doc("Workspace", module["name"], force=True)
            else:
                values = {
                    "custom_menu_title": module.get('title') or module.get('custom_menu_title') or '',
                    "custom_default_dashboard": module.get("custom_default_dashboard") or '',
                    "custom_open_dashboard": cint(module.get("custom_open_dashboard")),
                    "custom_hide_from_menu": cint(module.get("custom_hide_from_menu")),
                    "icon": module["icon"],
                    "sequence_id": int(module["sequence_id"]),
                    "parent_page": module.get("parent_page") or '',
                }
                if module.get('title'):
                    values["title"] = module['title']
                    values["label"] = module['title']
                frappe.db.set_value("Workspace", module["name"], values)
        else:
            if (module["_is_new"] == 'true'):
                workspace = frappe.new_doc("Workspace")
                workspace.title = module["title"]
                workspace.custom_menu_title = module["title"]
                workspace.custom_default_dashboard = module.get("custom_default_dashboard") or ''
                workspace.custom_open_dashboard = module.get("custom_open_dashboard") or 0
                workspace.custom_hide_from_menu = module.get("custom_hide_from_menu") or 0
                workspace.icon = module["icon"]
                workspace.content = module["content"]
                workspace.label = module["label"]
                workspace.sequence_id = int(module["sequence_id"])
                workspace.parent_page = module.get("parent_page") or ''
                workspace.for_user = ""
                workspace.public = 1
                workspace.save(ignore_permissions=True)

    return True


@frappe.whitelist()
def update_workspace_order(workspaces):
    workspaces_list = frappe.parse_json(workspaces)
    for workspace in workspaces_list:
        frappe.db.set_value('Workspace', workspace['name'], {
            'sequence_id': flt(workspace['sequence_id'])
        })
    return True


@frappe.whitelist()
def update_workspace_order_with_parent(workspaces):
    workspaces_list = frappe.parse_json(workspaces)
    for workspace in workspaces_list:
        frappe.db.set_value('Workspace', workspace['name'], {
            'sequence_id': flt(workspace['sequence_id']),
            'parent_page': workspace['parent_page']
        })
    return True


@frappe.whitelist()
def update_workspace_data(name, custom_title, icon):
    frappe.db.set_value("Workspace", name, {
        "custom_menu_title": custom_title,
        "icon": icon
    })
    return True


def clear():
    frappe.local.session_obj.update(force=True)
    frappe.local.db.commit()
    clear_user_cache(frappe.session.user)
    frappe.response['message'] = _("Cache Cleared")
