import requests
import frappe
import json

@frappe.whitelist()
def create_shopify_order(customer_email, items, shopify_url):
    
    items = json.loads(items)
    print(items)
    line_items = []

    for item in items:
        line_item = {
            "title": item.get("title"),
            "price": item.get("price"),
            "quantity": item.get("quantity"),
            "product_id": item.get("product_id"),
            "sku": item.get("sku"),
            "tax_lines": [
                {
                    "price": item.get("price") / 10,
                    "rate": 0.1,
                    "title": "SST",
                }
            ],
        }
        line_items.append(line_item)
    
    print(line_items)
    # Construct the API payload
    payload = {
        "order": {
            "email": customer_email,
            "financial_status": "pending",
            "fulfillment_status": "unfulfilled",
            "line_items": line_items,
        }
    }

    payload_json = json.dumps(payload)

    endpoint = 'orders.json'
    # Shopify API headers and endpoint
    headers = {
        "Content-Type": "application/json",
    }
    final_url = shopify_url + endpoint

    # Send the POST request to create the product
    response = requests.post(final_url, data=payload_json, headers=headers)

    if response.status_code == 201:
        frappe.msgprint(f"Order created in Shopify.")
    else:
        frappe.msgprint("Failed to create the order in Shopify. Error: {response.content}")
        print(response.status_code)

