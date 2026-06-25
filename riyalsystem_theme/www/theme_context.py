# Shared Theme Settings context for website pages (login, message, 404, error, etc.)

import frappe
from frappe import _


def get_web_theme_context():
	"""Return logo, colors and font from Theme Settings for public website pages."""
	logo = (
		frappe.db.get_single_value("Theme Settings", "login_page_logo")
		or "/assets/riyalsystem_theme/images/riyal-logo-default.svg"
	)
	app_name = (
		frappe.db.get_single_value("Website Settings", "app_name")
		or frappe.get_system_settings("app_name")
		or _("Riyal System")
	)

	theme_color_raw = frappe.db.get_single_value("Theme Settings", "theme_color") or "Blue"
	theme_color_key = theme_color_raw.replace(" ", "-").lower()
	palette = {
		"blue": ("#007BFF", "#0065cd"),
		"green": ("#43a047", "#2a7e2e"),
		"red": ("#e53935", "#be2724"),
		"orange": ("#fb8c00", "#d07706"),
		"yellow": ("#ffca28", "#deae1b"),
		"pink": ("#ec407a", "#b92a5a"),
		"violet": ("#ab47bc", "#773183"),
		"dark-gray": ("#38414b", "#24272e"),
	}
	primary, primary_hover = palette.get(theme_color_key, palette["blue"])
	font_family = frappe.db.get_single_value("Theme Settings", "font_family") or "Cairo"

	return {
		"logo": logo,
		"app_name": app_name,
		"primary_color": primary,
		"primary_hover": primary_hover,
		"font_family": font_family,
	}


# Bundled login-card slideshow when Theme Settings has no login card image(s).
DEFAULT_LOGIN_CARD_SLIDES = [
	"/assets/riyalsystem_theme/images/login-card-slides/slide-1.png",
	"/assets/riyalsystem_theme/images/login-card-slides/slide-2.png",
	"/assets/riyalsystem_theme/images/login-card-slides/slide-3.png",
	"/assets/riyalsystem_theme/images/login-card-slides/slide-4.png",
	"/assets/riyalsystem_theme/images/login-card-slides/slide-5.png",
]


def get_default_login_card_images():
	return list(DEFAULT_LOGIN_CARD_SLIDES)
