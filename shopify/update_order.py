import requests
import frappe
import json

@frappe.whitelist()
def update_shopify_order(orderID, status, shopify_url):

    paid_status = ""
    fulfil_status = ""
    print(status)
    if status == "To Deliver":
        paid_status = "paid"
        fulfil_status = "unfulfilled"
    elif status == "Completed":
        paid_status = "paid"
        fulfil_status = "fulfilled"
    print(paid_status)
    print(fulfil_status)
    
    # Construct the API payload
    payload = {
        "order": {
            "id": str(orderID),
            "tags": "best, on-time",
            "financial_status": paid_status,
            "fulfillment_status": fulfil_status,
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'orders/' + str(orderID) + '.json'
    final_url = shopify_url + endpoint

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Send the PUT request to create the product
        response = requests.put(final_url, data=payload_json, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        
        if response.status_code == 200:
            frappe.msgprint(f"Order was succefully updated in Shopify.")
        else:
            error_message = response.text 
            frappe.msgprint(f"Shopify API returned a non-success status code: {response.status_code}. Error message: {error_message}")
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        frappe.msgprint(f"An error occurred while making the Shopify API request: {str(e)}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    update_shopify_order(doc.order_id, doc.workflow_state, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Sales Order').on_submit = on_submit
