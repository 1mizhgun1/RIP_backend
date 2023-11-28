from django.db.models import Min, Max

from ..models import OpticItem

from .rus_names import rusNames
from .parse_request import *

def getTypeNames():
    return OpticItem.objects.values_list('type', flat=True).distinct()

# def getTypeList(activeEngName):
#     types = []
#     cnt = 0
#     for engName in getTypeNames():
#         cnt += 1
#         types.append({
#             'id': cnt,
#             'name': rusNames[engName],
#             'engName': engName,
#             'active': engName == activeEngName
#         })
#     return types

def getPrices(productList, request):
    if len(productList) == 0:
        return {
            'priceMin': 0,
            'priceMax': 0,
            'priceMinAbsolute': 0,
            'priceMaxAbsolute': 0
        }
    priceMinAbsolute = productList.aggregate(Min('price'))['price__min']
    priceMaxAbsolute = productList.aggregate(Max('price'))['price__max']
    prices = parsePrices(request)
    return {
        'priceMin': max(prices['price_min'], priceMinAbsolute),
        'priceMax': min(prices['price_max'], priceMaxAbsolute),
        'priceMinAbsolute': priceMinAbsolute,
        'priceMaxAbsolute': priceMaxAbsolute
    }

def getParams(product):
    params = []
    props = product.__dict__
    for key in props.keys():
        if key.startswith('param_') and props[key] != 'NULL':
            params.append({
                'key': rusNames[key],
                'value': props[key]
            })
    return params