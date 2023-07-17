// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tenant Bill Overview', {
	previous_electrical_unit: function(frm) {
		frm.set_value("unit_consumed", frm.doc.current_electrical_unit - frm.doc.previous_electrical_unit)
	},
	current_electrical_unit: function(frm) {
		frm.set_value("unit_consumed", frm.doc.current_electrical_unit - frm.doc.previous_electrical_unit)
	}
});
