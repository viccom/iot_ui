# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from math import ceil
from frappe import _

from iot.iot.doctype.iot_device.iot_device import IOTDevice
from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_user_groups as _list_user_groups
from cloud.cloud.doctype.cloud_company.cloud_company import list_user_companies
from iot.hdb_api import list_iot_devices
from iot_ui.ui_api import devices_list_array


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect
	filter = frappe.form_dict.filter
	# print(filter)
	if not filter:
		filter = "all"
	context.filter = filter
	context.no_cache = 1
	context.show_sidebar = True

	context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
	context.csrf_token = frappe.local.session.data.csrf_token

	if 'Company Admin' in frappe.get_roles(frappe.session.user):
		context.isCompanyAdmin = True
	userdevices = devices_list_array()
	# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", userdevices)

	if userdevices:
		context.userdevices = devices_list_array()
		context.dev_lens = int(ceil(len(devices_list_array())*0.1))
	else:
		context.userdevices = []
		context.dev_lens = 0
	context.title = _('weui_devices')
