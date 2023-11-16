import frappe
from shopify.retrieve_order import retrieve_shopify_orders

@frappe.whitelist()
def execute():
    try:
        shopify_link = frappe.get_all('Shopify Access', filters={'shopify_account': 'Main'}, fields=['name'])
        link = shopify_link[0]["name"]
        shopify_doc = frappe.get_doc("Shopify Access", link)
        api_key = shopify_doc.api_key
        api_token = shopify_doc.access_token
        api_link = shopify_doc.shopify_url
        retrieve_shopify_orders(api_key, api_token, api_link)
        frappe.msgprint("Hourly Orders Updated")
    except Exception as e:
        frappe.msgprint(f"Error in hourly execute function: {e}")