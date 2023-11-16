import requests
import frappe
import json

@frappe.whitelist()
def create_shopify_product(itemCode, itemName, itemStatus, itemDescription, price, unitWeight, inventoryNum, shopify_url, imagePath):
    # Construct the API payload without the image
    payload = {
        "product": {
            "title": itemName,
            "body_html": itemDescription,
            "vendor": "TD Furniture",
            "status": itemStatus,
            "variants": [
                {
                    "price": price,
                    "sku": itemCode,
                    "weight": unitWeight,
                    "inventory_management": "shopify",
                    "weight_unit": "kg",
                    "inventory_quantity": inventoryNum,
                    "old_inventory_quantity": inventoryNum,
                }
            ]
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'products.json'
    # Shopify API headers and endpoint
    headers = {
        "Content-Type": "application/json",
    }
    final_url = shopify_url + endpoint

    # Send the POST request to create the product without the image
    response = requests.post(final_url, data=payload_json, headers=headers)

    if response.status_code == 201:
        frappe.msgprint(f"Product '{itemName}' created in Shopify.")

        product_data = response.json()
        product_id = product_data["product"]["id"]
        
        # Update the product to add the image
        image_upload_endpoint = f'products/{product_id}.json'
        image_upload_url = shopify_url + image_upload_endpoint
        image_payload = {
            "product": {
                "id": product_id,
                "images": [{"src": imagePath}]
            }
        }
        
        image_payload_json = json.dumps(image_payload)
        image_response = requests.put(image_upload_url, data=image_payload_json, headers=headers)

        if image_response.status_code == 200:
            frappe.msgprint(f"Image added to the product '{itemName}' in Shopify.")
        else:
            frappe.msgprint(f"Failed to add the image to the product in Shopify. Error: {image_response.content}")

    else:
        frappe.msgprint(f"Failed to create the product in Shopify. Error: {response.content}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    create_shopify_product(doc.item_code, doc.item_name, doc.prod_status, doc.description, doc.standard_rate, doc.weight_per_unit, doc.opening_stock, doc.api_link, doc.image)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Item').on_submit = on_submit
