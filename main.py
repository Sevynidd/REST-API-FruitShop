import requests
import json
import sqlite3

from objects.product import Product
from objects.vendor import Vendor

products = []
vendors = []


def get_products_from_api():
    response = requests.get("https://api.predic8.de/shop/v2/products?limit=1000")
    if response.status_code == 200:
        response_json = response.json()

        for item in response_json["products"]:
            product = Product(int(item["id"]), item["name"])
            products.append(product)

    else:
        print("Fehlercode bei Api-Abfrage: " + str(response.status_code))


def get_productinfo_from_api():
    for product in products:
        response = requests.get(f"https://api.predic8.de/shop/v2/products/{product.id}")
        if response.status_code == 200:
            response_json = response.json()

            product.price = response_json["price"]
            for vendor in response_json["vendors"]:
                product.vendor_ids = vendor["id"]

        else:
            print("Fehlercode bei Api-Abfrage: " + str(response.status_code))


def get_vendors_from_api():
    response = requests.get("https://api.predic8.de/shop/v2/vendors?limit=1000")
    if response.status_code == 200:
        response_json = response.json()

        for item in response_json["vendors"]:
            vendor = Vendor(int(item["id"]), item["name"])
            vendors.append(vendor)

    else:
        print("Fehlercode bei Api-Abfrage: " + str(response.status_code))


def database_communication():
    con = sqlite3.connect("fruitshop.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS vendor(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, price REAL, "
                "vendor_id INTEGER, FOREIGN KEY(vendor_id) REFERENCES vendor(id))")


if __name__ == '__main__':
    get_products_from_api()
    get_productinfo_from_api()
    get_vendors_from_api()
    database_communication()
