import requests
import frappe
import json

@frappe.whitelist()
def update_shopify_product(item_code, shopify_id, api_link, qty):

    # Construct the API payload
    payload = {
        "product": {
            "vendor": "TD Furniture",
            "variants": [
                {
                    "sku": item_code,
                    "weight_unit": "kg",
                    "inventory_management": "shopify",
                    "inventory_quantity": qty,
                }
            ]
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'products/' + str(shopify_id) + '.json'
    headers = {
        'Content-Type': 'application/json',
    }
    final_url = api_link + endpoint

    # Send the PUT request to create the product
    response = requests.put(final_url, data=payload_json, headers=headers)

    if response.status_code == 200:
        frappe.msgprint(f"Product Quantity updated in Shopify.")
    else:
        frappe.msgprint(f"Failed to update the product in Shopify. Error: {response.content}")
        
