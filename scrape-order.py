import re
from bs4 import BeautifulSoup as BS
from tabulate import tabulate


def list_products(soup):
    products: list[dict] = []
    product_wrappers = soup.find_all('li', class_='product-list--list-item')

    for product in product_wrappers:
        name = product.find('a', {'data-auto': 'product-tile--title'}).text
        name = re.sub('\n *', ' ', name)
        cost = product \
            .find('div', class_='price-per-sellable-unit') \
            .find('span', class_='value').text
        items = product \
            .find('div', class_='quantity-label').text
        cost_per_vol = product \
            .find('div', class_='price-per-quantity-weight') \
            .find('span', class_='value').text

        products.append({'name': name, 'cost': "£{:,.2f}".format(float(cost)), 'items': items,
                        'cost_per_vol': "£{:,.2f}".format(float(cost_per_vol)).rjust(20, " ")})

    return products


with open("order.html") as file:
    soup = BS(file, 'lxml')

products = list_products(soup)

print(tabulate(products, tablefmt="presto", headers="keys"))

file = open("order-output.html", "w+")
file.write('<link rel="stylesheet" type="text/css" href="./order-output.css"  />')
file.write(tabulate(products, tablefmt="html", headers="keys"))
file.close()
