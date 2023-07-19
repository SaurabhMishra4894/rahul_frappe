# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document
from datetime import datetime
from six import string_types

from frappe import responses


class PropertyOverview(Document):
	def after_insert(self):
		tenants = frappe.db.get_all("Tenant", fields="*", filters={"status": "Active Tenant",
																   "concerned_property": self.property})
		for tenant in tenants:
			tenant_overview = frappe.new_doc("Tenant Bill Overview")
			property = frappe.get_doc("Property", tenant.concerned_property)
			if frappe.db.exists("Tenant Bill Overview",
								{"rent_year": self.year, "rent_month": self.month, "tenant": tenant.name}):
				tenant_overview = frappe.get_doc("Tenant Bill Overview",
												 {"rent_year": self.year, "rent_month": self.month,
												  "tenant": tenant.name})
			tenant_overview.tenant = tenant.name
			tenant_overview.rent_year = self.year
			tenant_overview.rent_month = self.month
			tenant_overview.tenant_name = tenant.tenant_name
			tenant_overview.concerned_property = tenant.concerned_property
			tenant_overview.occupied_room = tenant.occupied_room
			tenant_overview.base_rent = tenant.base_rent
			tenant_overview.previous_electrical_unit = ""
			tenant_overview.current_electrical_unit = ""
			tenant_overview.unit_consumed = ""
			tenant_overview.charge_per_unit = property.charge_per_unitelectricity
			tenant_overview.total_electrical_bill = ""
			tenant_overview.misc_charges = ""
			tenant_overview.total_rent = ""
			tenant_overview.amount_paid = ""
			tenant_overview.dues = ""
			tenant_overview.mode_of_payment = ""
			tenant_overview.date_of_payment = ""
			tenant_overview.paid_to = ""
			if property.divide_gas_and_water_bill_equally == "Yes":
				tenant_overview.gas_charges = float(self.total_gas_bills) / len(tenants)
				tenant_overview.water_charges = float(self.total_water_bills) / len(tenants)
				tenant_overview.electricity_charges = float(self.total_electical_bills) / len(tenants)
			tenant_overview.property_overview = self.name
			tenant_overview.save()
			frappe.db.commit()
		return {
			'status': 200,
			'message': "Successful",
		}


def perDayCost(property):
	property = frappe.get_doc("Property", property)
	tenants = frappe.db.get_all("Tenant", fields="*", filters={"status": "Active Tenant",
															   "concerned_property": property})
	for tenant in tenants:
		if frappe.db.exists("Tenant Bill Overview", {"tenant": tenant}):
			pass
		else:
			pass


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
	data = []
	property_list = frappe.db.get_all("Property", fields="*", filters={"payment_cycle_date": datetime.now().date().day})
	return property_list


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

		property_overview.gas_bill_name = (gas.get("first_name") if gas.get("first_name") else "") +\
										  " " + (gas.get("last_name") if gas.get("last_name") else "")
		property_overview.ca_number = gas.get("ca_number")
		property_overview.amount_before_due_date = gas.get("bill_due_before")
		property_overview.bill_date = gas.get("bill_date_is")
		property_overview.amount_after_due_date = gas.get("amount_after_due")
		property_overview.amount_to_be_paid = gas.get("amount_to_paid")
		# property_overview.total_demand = bses.get("total_demand")
		# property_overview.pending_settlement = bses.get("pending_settlement")
		# property_overview.installment_not_yet_due = bses.get("installment_not_yet_due")
		# property_overview.due_date = bses.get("due_date")
		# property_overview.total_payable = bses.get("total_amount")
		total_bses = 0.00
		for p_bses in bses:
			total_bses = total_bses + float(p_bses.get("total_amount"))
			property_overview.append('table_lscrr', {
				"total_demand": p_bses.get("total_demand") or 0,
				"pending_settlement": p_bses.get("pending_settlement") or 0,
				"installment_not_yet_due": p_bses.get("installment_not_yet_due") or "",
				"due_date": p_bses.get("due_date") or "",
				"total_payable": p_bses.get("total_amount") or 0
			})
		property_overview.total_dues = ""
		property_overview.total_collected_this_month = ""
		property_overview.total_electical_bills = total_bses
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
