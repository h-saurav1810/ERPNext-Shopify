import requests
import frappe
import json

@frappe.whitelist()
def cancel_shopify_order(orderID, shopify_url):

    endpoint = 'orders/' + str(orderID) + '/cancel.json'
    # Shopify API headers and endpoint
    headers = {
        "Content-Type": "application/json",
    }
    final_url = shopify_url + endpoint

    # Send the POST request to create the product
    response = requests.post(final_url, headers=headers)

    if response.status_code == 200:
        frappe.msgprint(f"Customer record was successfully cancelled in Shopify.")
    else:
        frappe.msgprint("Failed to delete the customer in Shopify. Error: {response.content}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    cancel_shopify_order(doc.order_id, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Sales Order').on_submit = on_submit
