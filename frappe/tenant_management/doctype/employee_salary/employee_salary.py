# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeSalary(Document):
	pass

@frappe.whitelist()
def fetch_employees(year,month):
	employees = frappe.get_list("Employee", fields="*", filters = {"status": "Active"})
	return employees
