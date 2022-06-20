import time
import math
import re
import requests
from bs4 import BeautifulSoup as BS


def product_sort(product):
    return product['cost_per_vol']


def get_page(site, page_num=None):
    headers = {'user-agent': 'my-app/0.0.1'}
    url = ''
    if not page_num:
        url = site
    else:
        url = f'{site}?page={page_num}'

    response = requests.get(url, headers=headers, allow_redirects=True)
    response.raise_for_status()
    content = response.text

    return BS(content, 'lxml')


def get_page_count(soup):
    product_count_string = soup.find(
        'div', {'data-auto': 'product-bin-count'}).find_all('strong')[1].text
    product_count = int(re.search(r'\d*', product_count_string).group(0))

    return math.ceil(product_count/48)


def list_products(soup, page_num):
    products = []
    product_wrappers = soup.find_all('li', class_='product-list--list-item')

    for product in product_wrappers:
        name = product.find('a', {'data-auto': 'product-tile--title'}).text
        cost_per_vol = product.find(
            'div', class_='price-per-quantity-weight').find('span', {'data-auto': 'price-value'}).text
        link = product.find('a', {'data-auto': 'product-tile--title'})['href']

        products.append({'name': name, 'cost_per_vol': float(
            cost_per_vol), 'page_num': page_num, 'link': f'https://www.tesco.com{link}'})

    return products


site = "https://www.tesco.com/groceries/en-GB/shop/drinks/wine/all"
products = []

first_page = get_page(site)
max_pages = get_page_count(first_page)

print(f"Page count: {max_pages}")

for page_num in range(1, max_pages + 1):
    time.sleep(0.1)
    page = get_page(site, page_num)
    page_products = list_products(page, page_num)
    products = products + page_products

products.sort(key=product_sort)

for product in products:
    print(product)
