import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:5000")
orders = []

@app.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    if "product_id" not in data:
        return jsonify(error="product_id is required"), 400

    product_id = data["product_id"]
    quantity = data.get("quantity", 1)

    try:
        resp = requests.get(f"{PRODUCT_URL}/products/{product_id}", timeout=3)
    except requests.RequestException:
        return jsonify(error="product-service unavailable"), 503

    if resp.status_code != 200:
        return jsonify(error="Product not found"), 404

    product = resp.json()
    order = {
        "id": len(orders) + 1,
        "product": product["name"],
        "quantity": quantity,
        "total": product["price"] * quantity,
    }
    orders.append(order)
    return jsonify(order), 201

@app.get("/orders")
def list_orders():
    return jsonify(orders)

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)