// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tenant Bill Overview', {
	previous_electrical_unit: function(frm) {
		frm.set_value("unit_consumed", frm.doc.current_electrical_unit - frm.doc.previous_electrical_unit);
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)

	},
	current_electrical_unit: function(frm) {
		frm.set_value("unit_consumed", frm.doc.current_electrical_unit - frm.doc.previous_electrical_unit);
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)
	},
	charge_per_unit: function(frm) {
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)
	},
	previous_dues: function(frm) {
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)
	},
	base_rent: function(frm) {
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)
	},
	unit_consumed: function(frm) {
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)
	},
	misc_charges: function(frm) {
		frm.set_value("total_rent", frm.doc.previous_dues + frm.doc.base_rent + (frm.doc.unit_consumed * frm.doc.charge_per_unit) + frm.doc.misc_charges)
	},
	total_rent: function(frm) {
		frm.set_value("dues", frm.doc.total_rent - frm.doc.amount_paid)
	},
	amount_paid: function(frm) {
		frm.set_value("dues", frm.doc.total_rent - frm.doc.amount_paid)
	}
});
