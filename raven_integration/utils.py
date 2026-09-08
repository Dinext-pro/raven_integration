from __future__ import annotations

import frappe


def active_apps() -> list[str]:
	"""Apps that currently run hooks on this site.

	Frappe >= 16 exposes ``get_active_apps`` (installed minus ``bench disable-app``).
	Frappe 15 only has ``get_installed_apps``; disable-app is not a platform API there.
	"""
	getter = getattr(frappe, "get_active_apps", None)
	if getter is not None:
		return getter()
	return frappe.get_installed_apps()


def raven_installed() -> bool:
	"""True if the Raven app is active on this site.

	Active, not merely installed: `bench disable-app raven` leaves the app in
	get_installed_apps() with its tables intact, and frappe itself switches to
	get_active_apps() to resolve hooks and to skip a disabled app's scheduled jobs.
	Anything else has the sweep adding and removing member rows in an app the site
	has turned off.
	"""
	return "raven" in active_apps()
