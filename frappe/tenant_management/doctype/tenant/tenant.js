// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tenant', {
	refresh: function (frm) {
		frm.add_custom_button(__("Full And Final"), function () {
			frappe.confirm(
				__('Are you sure to Do Full and Final for this Tenant?'),
				function () {
					show_alert('Processing Full and Final!')
					frappe.call({
						method: "frappe.tenant_management.doctype.tenant.tenant.full_and_final",
						args: {
							tenant: frm.doc.name
						},
						callback: function (r) {
							window.location.reload();
						}
					});
				},
				function () {
					window.close();
				}
			);
		});
	}
});
