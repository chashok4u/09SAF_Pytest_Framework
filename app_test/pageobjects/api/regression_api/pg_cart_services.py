import requests
import json

url = "https://ecommerce-apa-ppr.se.com/graphql"
headers = {
    'store': 'mexico_store_view',
    'Content-Type': 'application/json',
    'Cookie': 'PHPSESSID=839c2dba1f6c1455626f93264f58b78d; private_content_version=7ae003f0b686d6e5b1e7a03d428d9a95'
}


class product_cart:
    def create_empty_cart(self):
        payload = {
            "query": "mutation { createEmptyCart }"
        }

        response = requests.post(url, headers=headers, json=payload)

        response_json = response.json()
        create_empty_cart_value = response_json['data']['createEmptyCart']
        return create_empty_cart_value

    def fetch_cart_cart(self):
        cart_value = self.create_empty_cart()
        payload = {
            "query": f'{{ cart(cart_id: "{cart_value}") {{ id total_quantity items {{ id quantity product {{ sku }} }} }} }}',
            "variables": {}
        }
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        cart_id = response_json['data']['cart']['id']
        return cart_id

    def add_to_cart(self):
        cart_id = self.fetch_cart_cart()
        payload = {
            "query": f"""
                mutation {{
                    addProductsToCart(
                        cartId: "{cart_id}",
                        cartItems: [{{
                            quantity: 2,
                            sku: "QOD6S"
                        }}]
                    ) {{
                        cart {{
                            id
                            total_quantity
                            items {{
                                product {{
                                    name
                                    sku
                                    available_quantity
                                    salable_qty
                                }}
                                quantity
                            }}
                        }}
                        user_errors {{
                            code
                            message
                        }}
                    }}
                }}
            """,
            "variables": {}
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


cart = product_cart()
cart.add_to_cart()
