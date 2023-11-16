import requests
import frappe
import json

@frappe.whitelist()
def update_shopify_product(productID, itemCode, itemName, price, shopify_url):

    # Construct the API payload
    payload = {
        "product": {
            "title": itemName,
            "vendor": "TD Furniture",
            "variants": [
                {
                    "price": price,
                    "sku": itemCode,
                    "weight_unit": "kg",
                }
            ]
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'products/' + str(productID) + '.json'
    headers = {
        'Content-Type': 'application/json',
    }
    final_url = shopify_url + endpoint

    # Send the PUT request to create the product
    response = requests.put(final_url, data=payload_json, headers=headers)

    if response.status_code == 200:
        frappe.msgprint(f"Product '{itemName}' updated in Shopify.")
    else:
        frappe.msgprint(f"Failed to update the product in Shopify. Error: {response.content}")
        
# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    update_shopify_product(doc.product_id, doc.item_code, doc.item_name, doc.price_list_rate, doc.api_link)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Item').on_submit = on_submit
