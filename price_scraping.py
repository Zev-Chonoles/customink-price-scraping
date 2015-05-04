#!/usr/bin/env python

# Command-line arguments
import sys

# Sending and receiving HTTP requests
import requests

# HTML parsing
import BeautifulSoup as bs

max_quantity = int(sys.argv[1])
shirt_cut = sys.argv[2]

# Straight-cut ("Gildan Ultra Cotton T-shirt")
if shirt_cut == 's':
    product_id = '04617'
# Fitted ("Gildan Ladies 100% Cotton T-shirt")
if shirt_cut == 'f':
    product_id = '193619'

# Get a CSRF token for use in POST requests
request = requests.get('http://www.customink.com/quotes?product_id=' + product_id)
soup    = bs.BeautifulSoup(request.text)
token   = soup.find('input', {'name' : 'authenticity_token'})['value']

data = []

for quantity in range(1, max_quantity + 1):

    payload = {
        'authenticity_token' : token,
        'order[order_items_attributes][0][back_colors]' : '0',
        'order[order_items_attributes][0][front_colors]' : '1',
        'order[order_items_attributes][0][order_item_quantities_attributes][0][quantity]' : quantity,
        'order[order_items_attributes][0][order_item_quantities_attributes][0][size_id]' : '1',
        'order[order_items_attributes][0][product_id]' : product_id,
        'order[postal_code]' : '60637',
        'utf8' : '%%E2%%9C%%93'
    }

    request = requests.post('http://www.customink.com/quotes', data = payload)
    soup    = bs.BeautifulSoup(request.text)
    quote   = soup.find('div', {'class' : 'quoted-price'}).strong.contents[0][1:]

    data.append(quote)

print('\n'.join(data))