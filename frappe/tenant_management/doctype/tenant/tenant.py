# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class Tenant(Document):
	def validate(self):
		if self.concerned_property:
			properties = frappe.get_doc("Property", self.concerned_property)
			tenants_related = frappe.db.sql(
				"""SELECT sum(occupied_room) as total_occupied_room from `tabTenant` where status="Active Tenant" and concerned_property ='{concerned_property}'""".format(
					concerned_property=self.concerned_property), as_dict=True)
			if frappe.db.exists("Tenant", self.name):
				old_count = frappe.get_doc("Tenant", self.name)
				if len(tenants_related) > 0:
					if (tenants_related[0][
							"total_occupied_room"] or old_count.occupied_room - old_count.occupied_room or 0 + self.occupied_room or 0) > properties.total_room_available or 0:
						frappe.throw("Total Room Available for this property cannot be greater than Total Occupied Room")
					else:
						occupied_rooms = int(tenants_related[0][
											 "total_occupied_room"] or old_count.occupied_room) - int(old_count.occupied_room or 0) + int(self.occupied_room or 0)
						vacant_rooms = properties.total_room_available - (
							int(tenants_related[0]["total_occupied_room"] or old_count.occupied_room) - int(old_count.occupied_room or 0) + int(self.occupied_room or 0))
						frappe.db.sql("""UPDATE `tabProperty` set occupied_rooms={ocr}, vacant_rooms={vr}
						where name= '{name}';""".format(ocr=occupied_rooms, vr=vacant_rooms, name=self.concerned_property))
						frappe.db.commit()
				else:
					frappe.db.sql("""UPDATE `tabProperty` set occupied_rooms={ocr}, vacant_rooms={vr}
											where name= '{name}';""".format(ocr=self.occupied_room, vr=properties.total_room_available-self.occupied_room,
																			name=self.concerned_property))
					frappe.db.commit()


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
	# for po in property_overview:
	# 	po = frappe.get_doc("Property Overview" , po.name)
	# 	print("cs",po.total_collected)
	# 	total_income = total_income + int(po.total_collected or 0)
	# 	total_expense = total_expense + (int(po.total_electical_bills or 0) + int(po.total_gas_bills or 0) + int(po.total_water_bills or 0))
	# 	total_dues = total_dues + int(po.total_dues or 0)
	return {"total_data": {
		"total_income": 5000,
		"total_expenses": 400,
		"total_dues": 300
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


@frappe.whitelist()
def full_and_final(tenant):
	tenant = frappe.get_doc("Tenant", tenant)
	if tenant.status == "Active Tenant":
		tenant_overview_latest = frappe.db.sql("""
				SELECT * from `tabTenant Bill Overview` where tenant="{tenant}" order by creation DESC LIMIT 1
		""".format(tenant=tenant.name), as_dict=1)
		if len(tenant_overview_latest) > 0:
			tenant.full_and_final_amount = tenant_overview_latest[0]["dues"]
		else:
			tenant.full_and_final_amount = 0

		tenant.status = "Ex-tenant"
		tenant.save()
	else:
		return False
	return True
