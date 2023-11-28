from .parse_request import *

def filterType(productList, request):
    if 'type' in request.GET.keys():
        return productList.filter(type=request.GET['type'])
    return productList

def filterPrice(productList, request):
    prices = parsePrices(request)
    priceMin = prices['price_min']
    priceMax = prices['price_max']
    return productList.filter(price__range=[priceMin, priceMax])

def filterProducts(productList, request):
    return filterPrice(filterType(productList, request), request)