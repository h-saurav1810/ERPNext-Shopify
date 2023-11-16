from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Access"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Shopify Access",
					"description": _("Connection to Shopify."),
					"onboard": 1,
				},
            ]
        },
		{
			"label": _("Product Details"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Item Price",
					"description": _("Multiple Item prices."),
					"route": "#Report/Item Price",
					"dependencies": ["Item", "Price List"],
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Price List",
					"description": _("Price List master."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
					"onboard": 1,
					"dependencies": ["Item"],
				},
				{
					"type": "page",
					"name": "stock-balance",
					"label": _("Stock Summary"),
					"dependencies": ["Item"],
				},
			]
		},
		{
			"label": _("Customer Orders & Sales"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Customer",
					"description": _("Customer Database."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Quotation",
					"description": _("Quotes to Leads or Customers."),
					"onboard": 1,
					"dependencies": ["Item", "Customer"],
				},
				{
					"type": "doctype",
					"name": "Sales Order",
					"description": _("Confirmed orders from Customers."),
					"onboard": 1,
					"dependencies": ["Item", "Customer"],
				},
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Invoices for Costumers."),
					"onboard": 1,
					"dependencies": ["Item", "Customer"],
				},
			]
		},
		{
			"label": _("Delivery & Order Processing"),
			"items": [
				{
					"type": "doctype",
					"name": "Shipping Rule",
					"onboard": 1,
					"description": _("Rules for adding shipping costs."),
				},
				{
					"type": "doctype",
					"name": "Purchase Receipt",
					"onboard": 1,
					"dependencies": ["Item", "Supplier"],
				},
				{
					"type": "doctype",
					"name": "Delivery Note",
					"onboard": 1,
					"dependencies": ["Item", "Customer"],
				},
				{
					"type": "doctype",
					"name": "Delivery Trip",
					"onboard": 1,
					"dependencies": ["Item", "Customer"],
				},
			]
		},
    ]