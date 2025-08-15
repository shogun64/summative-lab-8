from flask import Flask, jsonify, request
from .api import fetch_product

app = Flask(__name__)

inventory = {"next_id": 1, "products": []}

@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory["products"]), 200

@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = next((i for i in inventory["products"] if i["id"] == id), None)
    if item is None:
        return jsonify({"message": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json() or {}
    name = data.get("product_name")
    if not name:
        return jsonify({"message": "Item name is required"}), 400
    item = {"id": inventory["next_id"], "product_name": name, "quantity": data.get("quantity", 0),
        "price": data.get("price"), "details": data.get("details", {})}
    inventory["products"].append(item)
    inventory["next_id"] += 1
    return jsonify(item), 201

@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    data = request.get_json() or {}
    item = next((i for i in inventory["products"] if i["id"] == id), None)
    if item is None:
        return jsonify({"message": "Item not found"}), 404
    for key in ("product_name", "quantity", "details"):
        if key in data:
            item[key] = data[key]
    return jsonify(item), 200

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = next((i for i in inventory["products"] if i["id"] == id), None)
    if not item:
        return ("Item not found", 404)
    inventory["products"] = [i for i in inventory["products"] if i["id"] != id]
    return "", 204

@app.route("/fetch", methods=["GET"])
def fetch():
    method = request.args.get('method')
    search = request.args.get('search')
    if not method:
        return jsonify({'message': 'Method required (barcode or name)'}), 400
    if not search:
        return jsonify({'message': 'Search data required'}), 400
    
    products = fetch_product(method, search)
    if not products:
        return jsonify({'message': 'No matching products found in API'}), 404
    return jsonify(products), 200

if __name__ == "__main__":
    app.run(debug=True)