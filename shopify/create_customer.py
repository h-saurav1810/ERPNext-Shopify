import requests
import frappe
import json

@frappe.whitelist()
def create_shopify_customer(firstName, lastName, mobileNum, emailID, address, addrCity, addrState, addrPostcode, shopify_url):

    # Construct the API payload
    payload = {
        "customer": {
            "email": emailID,
            "accepts_marketing": True,
            "first_name": firstName,
            "last_name": lastName,
            "orders_count": 0,
            "note": "",
            "tax_exempt": False,
            "tags": "",
            "currency": "MYR",
            "phone": "+60" + mobileNum,
            "addresses": [
                {
                "address1": address,
                "city": addrCity,
                "province": addrState,
                "country": "Malaysia",
                "zip": addrPostcode,
                "default": True,
                }
            ],
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'customers.json'
    # Shopify API headers and endpoint
    headers = {
        "Content-Type": "application/json",
    }
    final_url = shopify_url + endpoint

    try:
        # Send the POST request to create the product
        response = requests.post(final_url, data=payload_json, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        
        if response.status_code == 201:
            frappe.msgprint(f"Customer was created in Shopify.")
        else:
            frappe.msgprint(f"Shopify API returned a non-success status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        frappe.msgprint(f"An error occurred while making the Shopify API request: {str(e)}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    create_shopify_customer(doc.first_name, doc.last_name, doc.mobile_no, doc.email_id, doc.customer_address, doc.city, doc.state, doc.postcode, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Customer').on_submit = on_submit
