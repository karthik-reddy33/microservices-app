from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    1: {"id": 1, "name": "Laptop", "price": 55000},
    2: {"id": 2, "name": "Headphones", "price": 2500},
    3: {"id": 3, "name": "Keyboard", "price": 1800},
}

@app.get("/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))

@app.get("/products/<int:pid>")
def get_product(pid):
    product = PRODUCTS.get(pid)
    if not product:
        return jsonify(error="Product not found"), 404
    return jsonify(product)

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)