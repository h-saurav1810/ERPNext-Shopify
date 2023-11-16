import requests
import frappe
import json

@frappe.whitelist()
def delete_shopify_customer(customerID, shopify_url):

    endpoint = 'customers/' + str(customerID) + '.json'
    final_url = shopify_url + endpoint

    # Send the POST request to create the product
    response = requests.delete(final_url)
    response.raise_for_status() 

    if response.status_code == 200:
        frappe.msgprint(f"Customer record was deleted from Shopify.")
    else:
        frappe.msgprint("Failed to delete the customer in Shopify. Error: {response.content}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    delete_shopify_customer(doc.customer_id, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Customer').on_submit = on_submit
