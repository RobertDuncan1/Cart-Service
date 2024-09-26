import requests
from flask import *

app = Flask(__name__)

cart = [{"id": 0, "name": "apple", "price": 1.00, "amount": 1}]

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_products(user_id):
    if user_id == 1234:
        return jsonify({"products": cart})
    else:
        return jsonify({"error": "Cart not found"}), 404

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    if user_id == 1234:
        amount = request.json.get('amount')
        response = requests.get(f'https://product-service-zgf8.onrender.com/products/{product_id}')
        new_product = response.json()

        changed_amount = new_product['product']['amount'] - amount
        amount_to_send = {"amount": changed_amount}
        response = requests.post(f'https://product-service-zgf8.onrender.com/products/{product_id}', json=amount_to_send)
        data = response.json()
        print(data)

        new_product['product']['amount'] = amount
        cart.append(new_product['product'])
        return jsonify({"message": "Product added to cart", "product": new_product}), 201
    else:
        return jsonify({"error": "Cart not found"}), 404

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    if user_id == 1234:
        amount = request.json.get('amount')
        cart[product_id]["amount"] -= amount

        response = requests.get(f'http://https://product-service-zgf8.onrender.com/products/{product_id}')
        new_product = response.json()

        changed_amount = new_product['product']['amount'] + amount
        amount_to_send = {"amount": changed_amount}
        response = requests.post(f'https://product-service-zgf8.onrender.com/products/{product_id}', json=amount_to_send)
        data = response.json()
        print(data)

        return jsonify({"message": "Product removed from cart", "product": cart[product_id]}), 201
    else:
        return jsonify({"error": "Cart not found"}), 404




if __name__ == '__main__':
    app.run(debug=True,port=5001)



