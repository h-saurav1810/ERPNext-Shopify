import requests
import frappe
import json

@frappe.whitelist()
def delete_shopify_product(productID, shopify_url):

    endpoint = 'products/' + str(productID) + '.json'
    final_url = shopify_url + endpoint

    # Send the POST request to create the product
    response = requests.delete(final_url)

    if response.status_code == 200:
        frappe.msgprint(f"Product deleted from Shopify Account.")
    else:
        frappe.msgprint("Failed to delete the product in Shopify. Error: {response.content}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    delete_shopify_product(doc.product_id, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Item').on_submit = on_submit
