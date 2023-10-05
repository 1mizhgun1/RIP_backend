from django.shortcuts import render

from .data_processing.get_data import *
from .data_processing.filter_data import *

import requests

def GetProducts(request):
    productList = requests.get(URL + 'products/?status=A').json()
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': TYPES,
            'prices': getPrices()
        }
    })

def GetProduct(request, id):
    product = requests.get(URL + f'products/{id}/').json()
    return render(request, 'product.html', {
        'data' : {
            'id': id,
            'product': product,
            'types': TYPES,
            'params': getParams(product)
        }
    })

def GetType(request, engName):
    return render(request, 'products.html', {
        'data': {
            'products': filterType(engName),
            'types': getTypes(engName),
            'prices': getPrices(engName)
        }
    })

def GetFilteredProducts(request, engName='ALL'):
    prices = getPrices(engName)
    try:
        priceMin = int(request.GET['price_min'])
    except:
        priceMin = prices['priceMinAbsolute']
    try:
        priceMax = int(request.GET['price_max'])
    except:
        priceMax = prices['priceMaxAbsolute']
    prices['priceMin'] = priceMin
    prices['priceMax'] = priceMax
    if engName == 'ALL':
        productList = requests.get(URL + f'products/?status=A&price_min={priceMin}&price_max={priceMax}').json()
    else:
        productList = requests.get(URL + f'products/?status=A&type={engName}&price_min={priceMin}&price_max={priceMax}').json()
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': getTypes(engName),
            'prices': prices
        }
    })