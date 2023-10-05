import requests

rusNames = {'frames': 'Оправы для очков', 'sunglasses': 'Солнцезащитные очки', 'lenses': 'Контактные линзы', 'param_sex': 'Пол', 'param_material': 'Материал', 'param_type': 'Тип', 'param_color': 'Цвет оправы', 'param_form': 'Форма', 'param_time': 'Частота замены', 'param_brand': 'Бренд'}

def getTypeNames():
    return ['frames', 'sunglasses', 'lenses']

typeNames = getTypeNames()

URL = 'http://127.0.0.1:8080/'

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

def getPrices(engName='ALL'):
    if engName == 'ALL':
        prices = requests.get(URL + f'prices/?format=json&status=A').json()
    else:
        prices = requests.get(URL + f'prices/?format=json&status=A&type={engName}').json()
    priceMinAbsolute = prices['price_min']
    priceMaxAbsolute = prices['price_max']
    if priceMaxAbsolute == 10 ** 10:
        priceMaxAbsolute = 0
    return {
        'priceMin': priceMinAbsolute,
        'priceMax': priceMaxAbsolute,
        'priceMinAbsolute': priceMinAbsolute,
        'priceMaxAbsolute': priceMaxAbsolute
    }

def getParams(product):
    params = []
    for key in product.keys():
        if key.startswith('param_') and product[key] != 'NULL':
            params.append({
                'key': rusNames[key],
                'value': product[key]
            })
    return params