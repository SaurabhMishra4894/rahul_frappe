# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document
from datetime import datetime
from six import string_types

from frappe import responses


class PropertyOverview(Document):
	def after_save(self):
		tenants = frappe.db.get_all("Tenant", fields="*", filters= {"status": "Active Tenant",
			"concerned_property": self.name})
		for tenant in tenants:
			tenant_overview = frappe.new_doc("Tenant Overview")
			if frappe.db.exists("Tenant Overview", {"rent_year": self.year, "rent_month": self.month,"tenant":tenant.name}):
				tenant_overview = frappe.get_doc("Tenant Overview", {"rent_year": self.year, "rent_month": self.month,"tenant":tenant.name})


def create_tenants_overview():
	pass


def parse_args(args, error_message=None):
	try:
		if isinstance(args, string_types):
			return json.loads(args)
		return args
	except json.decoder.JSONDecodeError:
		return responses.send_error(error=error_message)
	except Exception:
		return responses.send_error(message=responses.RESPONSE_MESSAGES.get("BAD_REQUEST", ""))


@frappe.whitelist(allow_guest=True)
def return_property_list():
	frappe.session.user = "Administrator"
	data = frappe.db.get_all("Property", fields="*")
	return data


@frappe.whitelist(allow_guest=True)
def create_property_overview(**args):
	frappe.session.user = "Administrator"
	try:
		args = parse_args(args, responses.RESPONSE_MESSAGES.get("INVALID_OBJECT", "").format("args "))
		if type(args.get("data")) == str:
			args["data"] = json.loads(args.get("data"))

		data = args.get("data")
		property = frappe.get_doc("Property", data.get("property"))
		year = datetime.now().year
		month = datetime.now().strftime('%B')
		property_overview = frappe.new_doc("Property Overview")
		if frappe.db.exists("Property Overview", {"property": property.name, "year": year, "month": month}):
			property_overview = frappe.get_doc("Property Overview",
											   {"property": property.name, "year": year, "month": month})
		property_overview.year = year
		property_overview.month = month
		property_overview.property = property.name
		property_overview.property_name = property.property_name
		property_overview.property_address = property.property_address
		property_overview.occupied_rooms = property.occupied_rooms
		property_overview.vacant_rooms = property.vacant_rooms

		djb = data.get("djb")
		gas = data.get("gas")
		bses = data.get("bses")
		property_overview.bill_name = djb.get("bill_name")
		property_overview.bill_address = djb.get("bill_address")
		property_overview.water_bill_date = djb.get("bill_date")
		property_overview.bill_due_date = djb.get("bill_due")
		property_overview.bill_number = djb.get("bill_number")
		property_overview.bill_amount = djb.get("bill_amount")

		property_overview.gas_bill_name = gas.get("first_name") + " " + gas.get("last_name")
		property_overview.ca_number = gas.get("ca_number")
		property_overview.amount_before_due_date = gas.get("bill_due_before")
		property_overview.bill_date = gas.get("bill_date_is")
		property_overview.amount_after_due_date = gas.get("amount_after_due")
		property_overview.amount_to_be_paid = gas.get("amount_to_paid")

		property_overview.total_demand = bses.get("total_demand")
		property_overview.pending_settlement = bses.get("pending_settlement")
		property_overview.installment_not_yet_due = bses.get("installment_not_yet_due")
		property_overview.due_date = bses.get("due_date")
		property_overview.total_payable = bses.get("total_amount")

		property_overview.total_dues = ""
		property_overview.total_collected_this_month = ""
		property_overview.total_electical_bills = bses.get("total_amount")
		property_overview.total_gas_bills = gas.get("amount_to_paid")
		property_overview.total_water_bills = djb.get("bill_amount")

		property_overview.save()
		frappe.db.commit()

		return {
			'status': 200,
			'message': "Successful",
		}
	except BaseException as e:
		return {
			"status": 101,
			"error": frappe._(e)
		}
