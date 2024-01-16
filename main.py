import requests
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

    insert_vendors_query = "INSERT INTO vendor VALUES "

    for i in range(len(vendors)):
        insert_vendors_query += f"({vendors[i].id}, '{vendors[i].name}')"
        if i != (len(vendors) - 1):
            insert_vendors_query += ", "
    try:
        cur.execute(insert_vendors_query)
    except sqlite3.IntegrityError:
        print("Datenbank existiert schon. Bitte Datenbank entfernen.")
        exit(0)
    con.commit()

    insert_products_query = "INSERT INTO product VALUES "

    for j in range(len(products)):
        insert_products_query += f"({products[j].id}, '{products[j].name}', {products[j].price}, {products[j].vendor_ids})"
        if j != (len(products) - 1):
            insert_products_query += ", "

    cur.execute(insert_products_query)
    con.commit()


if __name__ == '__main__':
    get_products_from_api()
    get_productinfo_from_api()
    get_vendors_from_api()
    database_communication()

    userChoice = 0

    while True:
        try:
            userChoice = int(input("\n"
                                   "1. Ausgabe aller Produkte \n"
                                   "2. Ausgabe aller Händler \n"
                                   "3. Aufgeben einer Bestellung \n"
                                   "4. Beenden \n"
                                   "Eingabe: "))
        except ValueError:
            print("Falsche Eingabe\n")
            continue

        if userChoice == 1:
            for product in products:
                vendor_of_product = ""
                for vendor in vendors:
                    if vendor.id == product.vendor_ids:
                        vendor_of_product = vendor.name
                print(f"{product.id} - {product.name} {product.price}$ \n"
                      f"verkauft von {vendor_of_product}")
        elif userChoice == 2:
            for vendor in vendors:
                print(f"{vendor.id} - {vendor.name}")
        elif userChoice == 3:
            bestellung = input("Gib die IDs der Produkte mit einem Semikolon getrennt an:\n"
                               "Beispiel: 1;6;5"
                               "\n"
                               "IDs: ")

            bestellung_splitted = list(map(int, bestellung.split(";")))

            print("\n"
                  "===================================\n"
                  "         Bestellbestätigung\n"
                  "===================================\n")
            preis_summe = 0.0
            for product in products:
                if product.id in bestellung_splitted:
                    print(f"\t{product.id} - {product.name}\t\t {product.price}$")
                    preis_summe += product.price

            print("\n------------------------------------\n")
            print(f"\tSumme: {preis_summe}$")

        elif userChoice == 4:
            exit(0)
        else:
            print("Ungültige Eingabe")
