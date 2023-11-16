import requests
import frappe
import json

@frappe.whitelist()
def update_shopify_product(productID, itemCode, itemName, itemStatus, itemDescription, price, unitWeight, inventoryNum, shopify_url, imagePath):
    print(f"Received arguments - productID: {productID}, itemName: {itemName}, itemStatus: {itemStatus}, itemDescription: {itemDescription}, price: {price}, unitWeight: {unitWeight}, inventoryNum: {inventoryNum}, shopify_url: {shopify_url}")

    # Construct the API payload
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
                    "weight_unit": "kg",
                    "inventory_management": "shopify",
                    "inventory_quantity": inventoryNum,
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
            frappe.msgprint(f"Image updated with product '{itemName}' in Shopify.")
        else:
            frappe.msgprint(f"Failed to update the image with the product in Shopify. Error: {image_response.content}")

    else:
        frappe.msgprint(f"Failed to update the product in Shopify. Error: {response.content}")

# Attach the custom function to the 'Item' doctype's on_submit event
def on_submit(doc, method):
    update_shopify_product(doc.product_id, doc.item_code, doc.item_name, doc.prod_status, doc.description, doc.standard_rate, doc.weight_per_unit, doc.opening_stock, doc.api_link, doc.image)

# Ensure the on_submit function is triggered when an 'Item' document is submitted
frappe.get_doc('DocType', 'Item').on_submit = on_submit
