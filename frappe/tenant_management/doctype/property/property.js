// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property', {
	refresh: function (frm) {
		if (!frm.doc.__islocal) {
			// frappe.call({
			// 	method: "frappe.tenant_management.doctype.property.property.validateRoomCount",
			// 	args: {
			// 		"name": frm.doc.name
			// 	},
			// 	callback: function () {
			// 	}
			// });
		}
	},
	total_room_available: function (frm) {
		if (frm.doc.total_room_available < frm.doc.occupied_rooms){
			frappe.throw(__("Occupied Rooms can't be more than total room available!"));
		}
		frm.set_value("vacant_rooms", (frm.doc.total_room_available - frm.doc.occupied_rooms));
	},
	occupied_rooms: function (frm) {
		if (frm.doc.total_room_available < frm.doc.occupied_rooms){
			frappe.throw(__("Occupied Rooms can't be more than total room available!"));
		}
		frm.set_value("vacant_rooms", (frm.doc.total_room_available - frm.doc.occupied_rooms));
	}
});
