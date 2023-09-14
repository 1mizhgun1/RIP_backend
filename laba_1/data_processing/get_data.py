from django.db.models import Min, Max

from ..models import Product

rusNames = {'frames': 'Оправы для очков', 'sunglasses': 'Солнцезащитные очки', 'lenses': 'Контактные линзы', 'param_sex': 'Пол', 'param_material': 'Материал', 'param_type': 'Тип', 'param_color': 'Цвет оправы', 'param_form': 'Форма', 'param_time': 'Частота замены', 'param_brand': 'Бренд'}

def getTypeNames():
    return Product.objects.values_list('type', flat=True).distinct()

typeNames = getTypeNames()

def getTypes(activeEngName='ALL'):
    types = []
    cnt = 0
    for engName in typeNames:
        cnt += 1
        types.append({
            'id': cnt,
            'name': rusNames[engName],
            'engName': engName,
            'active': engName == activeEngName
        })
    return types

TYPES = getTypes()

def getPrices(productList):
    if len(productList) == 0:
        return {
            'priceMin': 0,
            'priceMax': 0,
            'priceMinAbsolute': 0,
            'priceMaxAbsolute': 0
        }
    priceMinAbsolute = productList.aggregate(Min('price'))['price__min']
    priceMaxAbsolute = productList.aggregate(Max('price'))['price__max']
    return {
        'priceMin': priceMinAbsolute,
        'priceMax': priceMaxAbsolute,
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