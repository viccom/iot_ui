# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from math import ceil
from frappe import _

from iot.iot.doctype.iot_device.iot_device import IOTDevice
from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_user_groups as _list_user_groups
from cloud.cloud.doctype.cloud_company.cloud_company import list_user_companies


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect
	context.no_cache = 1
	context.show_sidebar = True

	context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
	context.csrf_token = frappe.local.session.data.csrf_token

	if 'Company Admin' in frappe.get_roles(frappe.session.user):
		context.isCompanyAdmin = True

	wechatid = frappe.db.get_value("Wechat Binding", {"user": frappe.session.user})
	context.wechat_openid = None
	if wechatid:
		wechat_user_doc = frappe.get_doc("Wechat Binding", {"name": wechatid})
		context.wechat_openid = wechat_user_doc.openid
	context.user_id = frappe.session.user
	context.title = _('weui_devices')
