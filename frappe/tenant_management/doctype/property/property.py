# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Property(Document):
	def validate(self):
		if self.occupied_rooms > self.total_room_available:
			frappe.throw("Occupied rooms can't be greater than total room available")
		if self.total_room_available > 0:
			tenants_related = frappe.db.sql(
				"""SELECT sum(occupied_room) as total_occupied_room from `tabTenant` where status="Active Tenant" and concerned_property ='{concerned_property}'""".format(
					concerned_property=self.name), as_dict=True)
			occupied_room = tenants_related[0]["total_occupied_room"]
			if occupied_room:
				if occupied_room > self.total_room_available:
					frappe.throw("Total Room Available for this property cannot be greater than Total Occupied Room")
				self.occupied_rooms = occupied_room
				self.vacant_rooms = self.total_room_available - self.occupied_rooms

	def on_update(self):
		for property_room in self.property_rooms:
			tenant = frappe.get_doc("Tenant", property_room.assign_to)
			if tenant.room_number != property_room.room_name:
				tenant.room_number = property_room.room_name
				tenant.concerned_property = self.name
				tenant.save()
				frappe.db.commit()


@frappe.whitelist()
def validateRoomCount(name):
	properties = frappe.get_doc("Property", name)
	tenants_related = frappe.db.sql(
		"""SELECT sum(occupied_room) as total_occupied_room from `tabTenant` where status="Active Tenant" and concerned_property ='{concerned_property}'""".format(
			concerned_property=name), as_dict=True)
	if properties.total_room_available < tenants_related[0]["total_occupied_room"]:
		frappe.throw("Total Room Available for this property cannot be greater than Total Occupied Room")
