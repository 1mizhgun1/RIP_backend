from django.shortcuts import render

from .models import Product

from .data_processing.get_data import *
from .data_processing.filter_data import *

def GetProducts(request):
    productList = Product.objects.all()
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': getTypes(),
            'prices': getPrices(productList)
        }
    })

def GetProduct(request, id):
    product = Product.objects.get(pk=id)
    return render(request, 'product.html', {
        'data' : {
            'id': id,
            'product': product,
            'types': getTypes(),
            'params': getParams(product)
        }
    })

def GetType(request, engName):
    productList = filterType(engName)
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': getTypes(engName),
            'prices': getPrices(productList)
        }
    })

def GetFilteredProducts(request, engName='ALL'):
    productList = filterType(engName)
    prices = getPrices(productList)
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
    productList = filterPrice(productList, priceMin, priceMax)
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': getTypes(engName),
            'prices': prices
        }
    })

