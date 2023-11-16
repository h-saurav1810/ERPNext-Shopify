import requests
import base64
import frappe

@frappe.whitelist()
def retrieve_shopify_orders(api_key, api_password, shopify_store_url):
    # Construct the Shopify API endpoint for fetching orders
    order_items = []
    api_endpoint = shopify_store_url + "orders.json"

    # Set up the request headers with basic authentication
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{api_key}:{api_password}".encode()).decode(),
    }

    # Make the GET request to Shopify API
    try:
        response = requests.get(api_endpoint, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            orders_data = response.json().get("orders", [])

            # Process the retrieved orders
            if orders_data:
                for shopify_order in orders_data:
                    create_sales_order(shopify_order)  # Create order records in ERPNext

                frappe.msgprint("Shopify orders retrieved and new Sales Orders created in ERPNext.")
            else:
                frappe.msgprint("No orders retrieved from Shopify.")
        else:
            frappe.msgprint(f"Failed to fetch data from Shopify. Status code: {response.status_code}")

    except Exception as e:
        frappe.msgprint(f"An error occurred: {str(e)}")

def create_sales_order(shopify_order):
    order_name = shopify_order["name"]

    # Check if a Sales Order with the same title already exists in ERPNext
    existing_order = frappe.get_all('Sales Order', filters={'title': order_name}, fields=['name'])

    if not existing_order:
        new_sales_order = frappe.new_doc("Sales Order")
        new_sales_order.title = order_name
        new_sales_order.customer = shopify_order["email"]
        new_sales_order.set_warehouse = "Finished Goods - TDF"
        # new_sales_order.workflow_state = map_workflow_state(shopify_order)
        for line_item in shopify_order["line_items"]:
            create_sales_order_item(new_sales_order, line_item)

        new_sales_order.insert()  # Insert Sales Order record
    else:
        frappe.msgprint(f"Sales Order already exists in ERPNext.")

def map_workflow_state(shopify_order):
    if shopify_order["fulfillment_status"] == "unfulfilled":
        if shopify_order["financial_status"] == "pending":
            return "Draft"
        if shopify_order["financial_status"] == "paid":
            return "To Deliver"
    else:
        if shopify_order["financial_status"] == "pending":
            return "To Deliver"
        if shopify_order["financial_status"] == "paid":
            return "Completed"

def create_sales_order_item(sales_order, line_item):
    print(line_item)
    new_item = sales_order.append('items')
    shopify_id = line_item["product_id"]
    new_item.title = line_item["title"]
    new_item.item_code = line_item["sku"]
    new_item.shopify_id = shopify_id
    new_item.qty = int(line_item["quantity"])
    new_item.rate = float(line_item["price"])
    new_item.conversion_factor = 1.0  # Set the conversion factor

# Attach the custom function to the 'Sales Order' doctype's on_submit event
def on_submit(doc, method):
    retrieve_shopify_orders(doc.api_key, doc.api_token, doc.api_link)

# Ensure the on_submit function is triggered when a 'Sales Order' document is submitted
frappe.get_doc('DocType', 'Sales Order').on_submit = on_submit
