import requests
import json
import mysql.connector


def get_api_products():
    response = requests.get("https://api.predic8.de/shop/v2/products?limit=1000")
    if response.status_code == 200:
        response_json = response.json()

        for item in response_json["products"]:
            print(item["name"])

        mydb = mysql.connector.connect(
            host="localhost",
            user="karina",
            password=""
        )

        print(mydb)
    else:
        print("Fehlercode bei Api-Abfrage: " + str(response.status_code))


if __name__ == '__main__':
    get_api_products()
