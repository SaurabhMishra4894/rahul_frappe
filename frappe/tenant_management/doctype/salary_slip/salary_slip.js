// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Slip', {
	refresh: function(frm) {
        if (!frm.is_new()) {
            frm.disable_save();
        }
    }
});
