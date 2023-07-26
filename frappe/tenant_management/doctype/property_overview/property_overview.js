// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property Overview', {
	refresh: function (frm) {
		var tot_check = frm.doc.table_lscrr.length;
		for (var value in frm.doc.table_lscrr) {
			var data = frm.doc.table_lscrr[value];
			if (data.bill_attached == 1) {
				tot_check = tot_check - 1;
			}
		}

		if (frm.doc.status == "Open" && tot_check == 0) {
			frm.add_custom_button(__("Submit"), function () {
				// When this button is clicked, do this
				frm.set_value('status', "Submitted");
				frm.save();
			});
		}

	}
});
frappe.ui.form.on("Property Overview BSES", {
	bill_pdf: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.bill_pdf) {
			frappe.model.set_value(cdt, cdn, "bill_attached", 1);
		} else {
			frappe.model.set_value(cdt, cdn, "bill_attached", 0);
		}
	}
});
