# Copyright (c) 2021, Alyf GmbH and contributors
# Copyright (c) 2024, 4metrics Software GmbH and contributors

# import frappe
from frappe.model.document import Document

class JiraUser(Document):
	def autoname(self):
		self.name = f"{self.user} - {int(self.costing_rate + 0.5)}"
