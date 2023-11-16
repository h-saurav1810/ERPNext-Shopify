import requests
import base64
import frappe

@frappe.whitelist()
def retrieve_shopify_products(api_key, api_password, shopify_store_url):
    # Construct the Shopify API endpoint for fetching products
    api_endpoint = shopify_store_url + "products.json"

    # Set up the request headers with basic authentication
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{api_key}:{api_password}".encode()).decode(),
    }

    # Make the GET request to Shopify API
    try:
        response = requests.get(api_endpoint, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            products_data = response.json().get("products", [])

            # Process the retrieved products
            if products_data:
                product_list = []

                for shopify_product in products_data:
                    product_list.append(shopify_product)

                create_items(product_list)  # Create product records in ERPNext

                frappe.msgprint("Shopify products retrieved and new items created in ERPNext.")
            else:
                frappe.msgprint("No products retrieved from Shopify.")
        else:
            frappe.msgprint(f"Failed to fetch data from Shopify. Status code: {response.status_code}")

    except Exception as e:
        frappe.msgprint(f"An error occurred: {str(e)}")

def create_items(shopify_products):
    for shopify_product in shopify_products:
        item_code = shopify_product["variants"][0]["sku"]  # Adjust as per your Shopify product data

        # Check if a product with the same item code already exists in ERPNext
        existing_item = frappe.get_all('Item', filters={'item_code': item_code}, fields=['name'])

        if not existing_item:
            # Create a new item record in ERPNext
            new_item = frappe.new_doc("Item")
            new_item.item_code = item_code
            new_item.item_name = shopify_product["title"]
            new_item.product_id = shopify_product["id"]
            new_item.item_group = "Products"
            new_item.description = shopify_product["body_html"]
            new_item.prod_status = shopify_product["status"]
            new_item.standard_rate = shopify_product["variants"][0]["price"]
            new_item.weight_per_unit = shopify_product["variants"][0]["weight"]
            new_item.opening_stock = shopify_product["variants"][0]["inventory_quantity"]
            new_item.stock_uom = "Nos"
            new_item.weight_uom = "Nos"
            if shopify_product["image"] is not None:
                new_item.image = shopify_product["image"]["src"]
            new_item.insert()  # Insert product record
        else:
            # Item already exists, update its fields
            existing_item_name = existing_item[0]["name"]
            existing_item_doc = frappe.get_doc("Item", existing_item_name)
            existing_item_price_doc = frappe.get_doc("Item Price", existing_item_name)

            # Update fields with the new Shopify information
            existing_item_doc.item_name = shopify_product["title"]
            existing_item_doc.product_id = shopify_product["id"]
            existing_item_doc.description = shopify_product["body_html"]
            existing_item_doc.prod_status = shopify_product["status"]
            existing_item_price_doc.price_list_rate = shopify_product["variants"][0]["price"]
            existing_item_doc.weight_per_unit = shopify_product["variants"][0]["weight"]
            existing_item_doc.opening_stock = shopify_product["variants"][0]["inventory_quantity"]
            if shopify_product["image"] is not None:
                existing_item_doc.image = shopify_product["image"]["src"]
            existing_item_doc.save()  # Save the updated item record

            frappe.msgprint(f"Item with item code '{item_code}' in ERPNext updated with Shopify information.")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    retrieve_shopify_products(doc.apikey, doc.apitoken, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Item').on_submit = on_submit
