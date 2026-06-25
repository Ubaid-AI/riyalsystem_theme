# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import secrets
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import LDAPSettings
from frappe.utils.password import get_decrypted_password
from frappe.utils.html_utils import get_icon_html
from frappe.integrations.oauth2_logins import decoder_compat
from frappe.website.utils import get_home_page

no_cache = True


def get_context(context):
    redirect_to = frappe.local.request.args.get("redirect-to")

    if frappe.session.user != "Guest":
        if not redirect_to:
            if frappe.session.data.user_type == "Website User":
                redirect_to = get_home_page()
            else:
                redirect_to = "/app"

        if redirect_to != 'login':
            frappe.local.flags.redirect_location = redirect_to
            raise frappe.Redirect

    # get settings from site config
    context.no_header = True
    context.for_test = 'login.html'
    context["title"] = "Login"
    context["provider_logins"] = []
    context["disable_signup"] = frappe.utils.cint(frappe.db.get_single_value("Website Settings", "disable_signup"))
    context["logo"] = (frappe.db.get_single_value('Theme Settings', 'login_page_logo') or '/assets/riyalsystem_theme/images/riyal-logo-default.svg')
    context["app_name"] = (frappe.db.get_single_value('Website Settings', 'app_name') or frappe.get_system_settings("app_name") or _("Frappe"))

    # --- theme color + font for the login page (mirror the desk theme) ---
    theme_color_raw = frappe.db.get_single_value('Theme Settings', 'theme_color') or 'Blue'
    theme_color_key = theme_color_raw.replace(' ', '-').lower()
    theme_palette = {
        'blue': ('#007BFF', '#0065cd'),
        'green': ('#43a047', '#2a7e2e'),
        'red': ('#e53935', '#be2724'),
        'orange': ('#fb8c00', '#d07706'),
        'yellow': ('#ffca28', '#deae1b'),
        'pink': ('#ec407a', '#b92a5a'),
        'violet': ('#ab47bc', '#773183'),
        'dark-gray': ('#38414b', '#24272e'),
    }
    primary, primary_hover = theme_palette.get(theme_color_key, theme_palette['blue'])
    context["primary_color"] = primary
    context["primary_hover"] = primary_hover
    context["font_family"] = frappe.db.get_single_value('Theme Settings', 'font_family') or 'Cairo'

    # --- login card image(s): single photo, slideshow, or bundled default ---
    default_card_image = '/assets/riyalsystem_theme/images/login-card-default.png'
    card_type = frappe.db.get_single_value('Theme Settings', 'login_card_image_type') or 'Single Photo'
    card_images = []
    if card_type == 'Slideshow':
        rows = frappe.get_all(
            'Slideshow Photos',
            filters={'parent': 'Theme Settings', 'parentfield': 'login_card_slideshow'},
            fields=['photo'],
            order_by='idx asc',
        )
        card_images = [r.photo for r in rows if r.get('photo')]
    else:
        single = frappe.db.get_single_value('Theme Settings', 'login_card_photo')
        if single:
            card_images = [single]
    if not card_images:
        card_images = [default_card_image]
    context["login_card_images"] = card_images
    providers = [i.name for i in frappe.get_all("Social Login Key", filters={"enable_social_login": 1}, order_by="name")]
    for provider in providers:
        client_id, base_url = frappe.get_value("Social Login Key", provider, ["client_id", "base_url"])
        client_secret = get_decrypted_password("Social Login Key", provider, "client_secret")
        provider_name = frappe.get_value("Social Login Key", provider, "provider_name")

        icon = None
        icon_url = frappe.get_value("Social Login Key", provider, "icon")
        if icon_url:
            if provider_name != "Custom":
                icon = "<img src='{0}' alt={1}>".format(icon_url, provider_name)
            else:
                icon = get_icon_html(icon_url, small=True)

        if (get_oauth_keys(provider) and client_secret and client_id and base_url):
            context.provider_logins.append({
                "name": provider,
                "provider_name": provider_name,
                "auth_url": get_oauth2_authorize_url(provider, redirect_to),
                "icon": icon
            })
            context["social_login"] = True
    ldap_settings = LDAPSettings.get_ldap_client_settings()
    context["ldap_settings"] = ldap_settings

    login_label = [_("Email")]

    if frappe.utils.cint(frappe.get_system_settings("allow_login_using_mobile_number")):
        login_label.append(_("Mobile"))

    if frappe.utils.cint(frappe.get_system_settings("allow_login_using_user_name")):
        login_label.append(_("Username"))

    context['login_label'] = ' {0} '.format(_('or')).join(login_label)
    context['build_version_dev'] = secrets.randbits(50),

    return context


@frappe.whitelist(allow_guest=True)
def login_via_google(code, state):
    login_via_oauth2("google", code, state, decoder=decoder_compat)


@frappe.whitelist(allow_guest=True)
def login_via_github(code, state):
    login_via_oauth2("github", code, state)


@frappe.whitelist(allow_guest=True)
def login_via_facebook(code, state):
    login_via_oauth2("facebook", code, state, decoder=decoder_compat)


@frappe.whitelist(allow_guest=True)
def login_via_frappe(code, state):
    login_via_oauth2("frappe", code, state, decoder=decoder_compat)


@frappe.whitelist(allow_guest=True)
def login_via_office365(code, state):
    login_via_oauth2_id_token("office_365", code, state, decoder=decoder_compat)


@frappe.whitelist(allow_guest=True)
def login_via_token(login_token):
    sid = frappe.cache().get_value("login_token:{0}".format(login_token), expires=True)
    if not sid:
        frappe.respond_as_web_page(_("Invalid Request"), _("Invalid Login Token"), http_status_code=417)
        return

    frappe.local.form_dict.sid = sid
    frappe.local.login_manager = LoginManager()

    redirect_post_login(desk_user=frappe.db.get_value("User", frappe.session.user, "user_type") == "System User")
