from django.shortcuts import render

from .models import OpticItem

from .data_processing.get_data import *
from .data_processing.filter_data import *

from django.db import connection

def GetProducts(request):
    productList = OpticItem.objects.all().filter(status='A').order_by('last_modified')
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': TYPES,
            'prices': getPrices(productList)
        }
    })

def GetProduct(request, id):
    product = OpticItem.objects.get(pk=id)
    return render(request, 'product.html', {
        'data' : {
            'id': id,
            'product': product,
            'types': TYPES,
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

def DeleteFromProducts(request, engName='ALL'):
    id = -1
    if 'delete_card' in request.POST.keys():
        id = request.POST['delete_card']
    if id != -1:
        with connection.cursor() as cursor:
            cursor.execute("update laba_1_opticitem set status = 'N' where id = " + id)
    productList = filterType(engName)
    return render(request, 'products.html', {
        'data': {
            'products': productList,
            'types': getTypes(engName),
            'prices': getPrices(productList)
        }
    })