import requests
import sys
import urllib.request

URL = 'https://www.ocado.com/webshop/api/v1/search?searchTerm='

def get_product_details(product):
    product = product.replace(' ', '%20')
    url = URL + product
    json = requests.get(url).json()
    productArray = json["mainFopCollection"]["sections"][0]["fops"]
    return productArray

def make_product_list(product):
    productArray = get_product_details(product)
    productDict = {}
    for item in productArray:
        item = item["product"]
        productDict[item["name"]] = {
            "price" : item["price"]["current"],
            "unit price": item["price"]["unit"],
        }
    return productDict
