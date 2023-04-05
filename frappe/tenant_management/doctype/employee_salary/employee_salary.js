// Copyright (c) 2023, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Salary', {
	refresh: function (frm) {
		frm.cscript.fetch_employees_data = function (doc) {
			if (!doc.payment_year || !doc.payment_month) {
				frappe.throw("Please Provide Payment Year and Month");
			}
			frappe.call({
				method: "frappe.tenant_management.doctype.employee_salary.employee_salary.fetch_employees",
				args: {
					year: frm.doc.payment_year,
					month: frm.doc.payment_month
				}
			}).then((res) => {
				if (res.message) {
					frm.clear_table("employee_salary");
					for (var emp in res.message) {
						emp = res.message[emp];
						var a = frm.add_child("employee_salary");
						a.employee = emp.name;
						a.employee_name = emp.employee_name;
						a.base_salary = emp.salary;
						a.mode_of_payment = "Cash";
						refresh_field("employee_salary");
					}
				}
			});
		}
	}
});
frappe.ui.form.on('Employee Salaries', {
	misc_charges: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		row.total_salary = parseInt(row.misc_charges)+parseInt(row.base_salary);
		refresh_field("employee_salary");
	},
});
