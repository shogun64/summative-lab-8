import requests

def fetch_product(method, search):
    BASE_URL = "https://world.openfoodfacts.org"
    if method == "Name" or method == "name":
        URL = f"{BASE_URL}/cgi/search.pl"
        response = requests.get(URL, params={"search_terms": search,
                "json": 1, "page_size": 5})
        data = response.json()
        if data.get("products"):
            results = []
            for product in data.get("products", []):
                results.append({
                    "product_name": product.get("product_name", "Unknown"),
                    "brands": product.get("brands", "Unknown"),
                    "barcode": product.get("code", ""),
                    "ingredients_text": product.get("ingredients_text", "")
                })
            return {"success": True, "products": results}
    elif method == "Barcode" or method == "barcode":
        URL = f"{BASE_URL}/api/v2/product/{search}.json"
        response = requests.get(URL)
        data = response.json()
        if data.get("status") == 1:
            return {
                "success": True,
                "product": {
                    "product_name": data.get("product", {}).get("product_name", "Unknown"),
                    "brands": data.get("product", {}).get("brands", "Unknown"),
                    "ingredients_text": data.get("product", {}).get("ingredients_text", ""),
                    "image_url": data.get("product", {}).get("image_url", ""),
                    "nutriscore_grade": data.get("product", {}).get("nutriscore_grade", ""),
                    "categories": data.get("product", {}).get("categories", "")
                }
            }
    return None