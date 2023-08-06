## This script contains all function to scrape zatu data
import requests
from bs4 import BeautifulSoup
import csv
from decimal import Decimal

"""
Extract function:
1) It will print out the current scraping page number, 10 page in a row
2) Extract data by BeautifulSoup:
	- product_list = the section in the webpage that contains all the product
    - product = extract product data in product_list one by one
    - 
"""
def extract_data(z_url, z_page):
    full_products = []
    while True:
        line_end =".. "
        if z_page % 10 == 0 : line_end ='\n'
        print(f'{z_page}', end = line_end)
        url = f'{z_url}&page={z_page}&show=200'
        response = requests.get(url, headers = {'User-Agent': 'Mozilla/6.0'})
        soup = BeautifulSoup(response.content, "html.parser")
#        print(soup)
        product_list = soup.find("ul", class_='zg-products-list')
#        print(product_list)
        products = []
        if product_list != None and product_list.find_all("li", class_="zg-product"):
          for product in product_list.find_all("li", class_="zg-product"):
#              print(product)
              prdPrice = product.find_all("div", class_="zg-price-box-now")
              prdPriceWas = product.find_all("del", class_="zg-price-box-was")
              price_was = -1
              if len(prdPriceWas) >= 1 : price_was = prdPriceWas[0]["data-was"]
              product_data = {
                  "name": product.find("div", class_="zg-product-title").text,
                  "price": Decimal(prdPrice[0]["data-now"]),
                  "price_was": Decimal(price_was),
                  "notice": product.find("div", class_="zg-product-notice").text,
              }
              products.append(product_data)

        full_products.extend(products)
        if not products:
            break
        z_page += 1
    return full_products

def load2csv (product_list, csv_path, header):
    with open(csv_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(product_list)
    return ('===csv_exported===')
