# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeSalary(Document):
	def on_submit(self):
		for salary in self.employee_salary:
			salary_slip = frappe.new_doc("Salary Slip")
			salary_slip.employee_salary = self.name
			salary_slip.year = self.payment_year
			salary_slip.month = self.payment_month
			salary_slip.employee = salary.employee
			salary_slip.employee_name = salary.employee_name
			salary_slip.mode_of_payment = salary.mode_of_payment
			salary_slip.base_salary = salary.base_salary
			salary_slip.misc_charges = salary.misc_charges
			salary_slip.total_salary = salary.total_salary
			salary_slip.date_of_payment = salary.date_of_payment
			salary_slip.save()
			frappe.db.commit()

@frappe.whitelist()
def fetch_employees(year,month):
	employees = frappe.get_list("Employee", fields="*", filters = {"status": "Active"})
	return employees
