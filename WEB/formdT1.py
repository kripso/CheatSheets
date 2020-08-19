import requests
from bs4 import BeautifulSoup

URL = 'https://formdworks.com/products/t1'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='section-product')

div = results.find('div', id='add-to-cart-product')

button = div.find('button', type='submit')

print(button)
