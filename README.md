# Commands

```bash
python3 main.py add_item --name "Test" --quantity 0 --price 1.00 --details "N/A"
[Adds a new product to the database (quantity and details are optional)]

python3 main.py list_inventory
[Lists all products in the database]

python3 main.py find_item 1
[Finds a product with the id above in the database]

python3 main.py update_item 1 --quantity 1
[Updates the product with the id above with a new value (name, quantity, price, details)]

python3 main.py delete_item 1
[Deletes the product with the id above]

python3 main.py fetch --method barcode --search 3017624010701
python3 main.py fetch --method name --search Nutella
[Fetches a product or products from the Open Food Facts API using either a barcode or name]
```