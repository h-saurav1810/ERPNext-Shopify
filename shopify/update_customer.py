import requests
import frappe
import json

@frappe.whitelist()
def update_shopify_customer(customerID, firstName, lastName, mobileNum, emailID, address, addrCity, addrState, addrPostcode, customerNotes, customerTags, shopify_url):
    print(f"Received arguments - productID: {customerID}, fName: {firstName}, lName: {lastName}, mobile: {mobileNum}, email: {emailID}, address: {address}, city: {addrCity}, state: {addrState}, zip: {addrPostcode}, notes: {customerNotes}, tags: {customerTags}, shopify_url: {shopify_url}")

    # Construct the API payload
    payload = {
        "customer": {
            "email": emailID,
            "first_name": firstName,
            "last_name": lastName,
            "note": customerNotes,
            "tags": customerTags,
            "currency": "MYR",
            "phone": "+60" + mobileNum,
            "addresses": [
                {
                "address1": address,
                "city": addrCity,
                "province": addrState,
                "country": "Malaysia",
                "zip": addrPostcode,
                }
            ],
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'customers/' + str(customerID) + '.json'
    final_url = shopify_url + endpoint

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        # Send the PUT request to create the product
        response = requests.put(final_url, data=payload_json, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        
        if response.status_code == 200:
            frappe.msgprint(f"Customer record was updated in Shopify.")
        else:
            error_message = response.text 
            frappe.msgprint(f"Shopify API returned a non-success status code: {response.status_code}. Error message: {error_message}")
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        frappe.msgprint(f"An error occurred while making the Shopify API request: {str(e)}")


# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    update_shopify_customer(doc.customer_id, doc.first_name, doc.last_name, doc.mobile_no, doc.email_id, doc.customer_address, doc.city, doc.state, doc.postcode, doc.notes, doc.customer_tags, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Customer').on_submit = on_submit
