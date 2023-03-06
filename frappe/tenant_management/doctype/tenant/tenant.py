# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.tenant_management.doctype.property.property import validateRoomCount


class Tenant(Document):
	def validate(self):
		properties = frappe.get_doc("Property", self.concerned_property)
		tenants_related = frappe.db.sql(
			"""SELECT sum(occupied_room) as total_occupied_room from `tabTenant` where status="Active Tenant" and concerned_property ='{concerned_property}'""".format(
				concerned_property=self.concerned_property), as_dict=True)
		if frappe.db.exists("Tenant", self.name):
			old_count = frappe.get_doc("Tenant", self.name)
			if (tenants_related[0][
					"total_occupied_room"] - old_count.occupied_room + self.occupied_room) > properties.total_room_available:
				frappe.throw("Total Room Available for this property cannot be greater than Total Occupied Room")


@frappe.whitelist()
def tenant_data():
	year = datetime.now().year
	month = datetime.now().strftime('%B')
	property_overview = frappe.get_all("Property Overview", {"year": year, "month": month})
	tenant_overview = frappe.get_all("Tenant Bill Overview", {"rent_year": year, "rent_month": month})
	to_array = []
	for to in tenant_overview:
		to = frappe.get_doc("Tenant Bill Overview", to.name)
		if to.dues > 0:
			to_array.append({
				"tenant_id": to.name,
				"tenant_name": to.tenant_name,
				"property_name": to.concerned_property,
				"amount_due": to.dues
			})
	total_income = 0
	total_expense = 0
	total_dues = 0
	for po in property_overview:
		total_income += po.total_collected
		total_expense += (po.total_electical_bills + po.total_gas_bills + po.total_water_bills)
		total_dues += po.total_dues
	print("property overview", property_overview)
	return {"total_data": {
		"total_income": total_income,
		"total_expenses": total_expense,
		"total_dues": total_dues
	},
		"graph_data": {
			"income": [
				9000, 5000, 6000, 7000, 3000, 5000, 6000, 7300, 500,
				600, 3000, 500
			],
			"expenses": [
				500, 600, 700, 300, 500, 500, 600, 700,
				300, 500, 800, 500
			]
		},
		"tenant_dues": to_array}
