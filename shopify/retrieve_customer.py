import requests
import base64
import frappe

@frappe.whitelist()
def retrieve_shopify_customers(api_key, api_password, shopify_store_url):
    # Construct the Shopify API endpoint for fetching customers
    api_endpoint = shopify_store_url + "customers.json"

    # Set up the request headers with basic authentication
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{api_key}:{api_password}".encode()).decode(),
    }

    # Make the GET request to Shopify API
    try:
        response = requests.get(api_endpoint, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            customers_data = response.json().get("customers", [])

            # Process the retrieved customers
            if customers_data:
                customer_list = []

                for shopify_customer in customers_data:
                    customer_list.append(shopify_customer)

                create_items(customer_list)  # Create customer records in ERPNext

                frappe.msgprint("Shopify customers retrieved and created in ERPNext.")
            else:
                frappe.msgprint("No customers retrieved from Shopify.")
        else:
            frappe.msgprint(f"Failed to fetch data from Shopify. Status code: {response.status_code}")

    except Exception as e:
        frappe.msgprint(f"An error occurred: {str(e)}")

def create_items(shopify_customers):
    for shopify_customer in shopify_customers:
        email = shopify_customer["email"]

        # Check if a customer with the same email address already exists in ERPNext
        existing_customer = frappe.get_all('Customer', filters={'email_id': email}, fields=['name'])

        shopify_link = frappe.get_all('Shopify Access', filters={'shopify_account': 'Main'}, fields=['name'])
        link = shopify_link[0]["name"]

        shopify_doc = frappe.get_doc("Shopify Access", link)
        api_key = shopify_doc.api_key
        print(api_key)
        
        if not existing_customer:
            # Create a new customer record in ERPNext
            customer_record = frappe.new_doc("Customer")
            customer_record.email_id = email
            if shopify_customer["phone"] == "" or shopify_customer["phone"] == None:
                customer_record.mobile_no = "-"
            else:
                customer_record.mobile_no = shopify_customer["phone"]
            customer_record.customer_id = shopify_customer["id"]
            customer_record.first_name = shopify_customer["first_name"]
            if shopify_customer["last_name"] == "" or shopify_customer["last_name"] == None:
                customer_record.last_name = "-"
            else:
                customer_record.last_name = shopify_customer["last_name"]
            customer_record.customer_address = shopify_customer["addresses"][0]["address1"]
            customer_record.city = shopify_customer["addresses"][0]["city"]
            if shopify_customer["addresses"][0]["province"] == "" or shopify_customer["addresses"][0]["province"] == None:
                customer_record.state = "-"
            else:
                customer_record.state = shopify_customer["addresses"][0]["province"]
            customer_record.postcode = shopify_customer["addresses"][0]["zip"]
            customer_record.default_currency = "MYR"
            customer_record.default_price_list = "Standard Selling"
            customer_record.customer_group = "All Customer Groups"
            customer_record.customer_type = "Individual"
            customer_record.tax_category = "Standard Tax"
            customer_record.insert()  # Insert customer record
        else:
            # Customer already exists, update its fields
            existing_customer_name = existing_customer[0]["name"]
            existing_customer_doc = frappe.get_doc("Customer", existing_customer_name)

            # Update fields with the new Shopify information
            existing_customer_doc.email_id = email
            existing_customer_doc.mobile_no = shopify_customer["phone"]
            existing_customer_doc.customer_id = shopify_customer["id"]
            existing_customer_doc.first_name = shopify_customer["first_name"]
            existing_customer_doc.last_name = shopify_customer["last_name"]
            existing_customer_doc.customer_address = shopify_customer["addresses"][0]["address1"]
            existing_customer_doc.city = shopify_customer["addresses"][0]["city"]
            existing_customer_doc.state = shopify_customer["addresses"][0]["province"]
            existing_customer_doc.postcode = shopify_customer["addresses"][0]["zip"]
            existing_customer_doc.save()  # Save the updated customer record

            frappe.msgprint(f"Customer '{email}' in ERPNext updated with Shopify information.")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    retrieve_shopify_customers(doc.apikey, doc.apitoken, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Customer').on_submit = on_submit
