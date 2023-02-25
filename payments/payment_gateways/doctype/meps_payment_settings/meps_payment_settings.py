# Copyright (c) 2023, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.integrations.utils import create_request_log
from frappe.model.document import Document
from frappe import _
from urllib.parse import urlencode
from frappe.utils import (
	get_url,
)

class MEPSPaymentSettings(Document):
	supported_currencies = ["USD", "JOD"]
	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_(
					"Please select another payment method. MEPS does not support transactions in currency '{0}'"
				).format(currency)
			)

	def get_payment_url(self, **kwargs):
		"""Return payment url with several params"""
		# create unique order id by making it equal to the integration request
		integration_request = create_request_log(kwargs, service_name="MEPS")
		kwargs.update(dict(order_id=integration_request.name))

		return get_url(f"./paytm_checkout?{urlencode(kwargs)}")