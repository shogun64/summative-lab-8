import argparse
import requests

API_BASE_URL = "http://127.0.0.1:5555/"

def add_item(args):
    item = {'product_name': args.name, 'quantity': args.quantity, 'price': args.price, 'details': args.details}
    try:
        response = requests.post(f"{API_BASE_URL}/inventory", json=item)
        response.raise_for_status()
        print("Item added:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def list_inventory(args):
    try:
        response = requests.get(f"{API_BASE_URL}/inventory")
        response.raise_for_status()
        items = response.json()
        
        if not items:
            print("No items in inventory.")
            return
        
        print(f"Total items: {len(items)}")
        for item in items:
            print(f"ID: {item['id']} | {item['product_name']} | Qty: {item['quantity']} | Price: ${item['price']}\nDetails: {item['details']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def find_item(args):
    try:
        response = requests.get(f"{API_BASE_URL}/inventory/{args.id}")
        response.raise_for_status()
        item = response.json()
        
        print(f"ID: {item['id']} | {item['product_name']} | Qty: {item['quantity']} | Price: ${item['price']}\nDetails: {item['details']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def update_item(args):
    item = {}
    if args.name:
        item['product_name'] = args.name
    if args.quantity:
        item['quantity'] = args.quantity
    if args.price:
        item['price'] = args.price
    if args.details:
        item['details'] = args.details
    try:
        response = requests.patch(f"{API_BASE_URL}/inventory/{args.id}", json=item)
        response.raise_for_status()
        print("Item updated:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def delete_item(args):
    try:
        response = requests.delete(f"{API_BASE_URL}/inventory/{args.id}")
        response.raise_for_status()
        print("Item deleted.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def fetch(args):
    params = {"method": args.method, "search": args.search}
    try:
        response = requests.get(f"{API_BASE_URL}/fetch", params=params)
        response.raise_for_status()
        if "products" in response.json():
            print("Items fetched:")
            for product in response.json()["products"]:
                for item in product:
                    print(f"{item}: {product[item]}")
                print("\n")
        elif "product" in response.json():
            print("Item fetched:", response.json()["product"]["product_name"])
            for item in response.json()["product"]:
                if item != "product_name":
                    print(f"{item}: {response.json()["product"][item]}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def setup_parser():
    parser = argparse.ArgumentParser(description="Inventory CLI")
    sub = parser.add_subparsers()

    add_item_parser = sub.add_parser("add_item")
    add_item_parser.add_argument("--name", required=True)
    add_item_parser.add_argument("--quantity", default="0")
    add_item_parser.add_argument("--price", required=True)
    add_item_parser.add_argument("--details", default="N/A")
    add_item_parser.set_defaults(func=add_item)

    list_parser = sub.add_parser("list_inventory")
    list_parser.set_defaults(func=list_inventory)

    find_parser = sub.add_parser("find_item")
    find_parser.add_argument("id", type=int)
    find_parser.set_defaults(func=find_item)

    update_parser = sub.add_parser("update_item")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--name")
    update_parser.add_argument("--quantity")
    update_parser.add_argument("--price")
    update_parser.add_argument("--details")
    update_parser.set_defaults(func=update_item)
    
    delete_parser = sub.add_parser("delete_item")
    delete_parser.add_argument("id", type=int)
    delete_parser.set_defaults(func=delete_item)

    fetch_parser = sub.add_parser("fetch")
    fetch_parser.add_argument("--method", required=True)
    fetch_parser.add_argument("--search", required=True)
    fetch_parser.set_defaults(func=fetch)

    return parser

if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()