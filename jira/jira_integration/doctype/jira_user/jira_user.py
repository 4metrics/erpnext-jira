# Copyright (c) 2021, Alyf GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class JiraUser(Document):
	def autoname(self):
		self.name = f"{self.user} - {int(self.costing_rate + 0.5)}"
