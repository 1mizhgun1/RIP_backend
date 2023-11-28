from django.shortcuts import render

def getDatabase():
    return {'data' : {
        'products': [{
                'id': 1,
                'row': [{'title': 'Оправа для очков TOMMY HILFIGER TH 1772 PJP', 'id': 1, 'image': 'images/frame_1.jpg', 'price': 7200, 'status': 'в наличии', 'type': 'frames', 'params': {'Пол': 'Мужские', 'Материал': 'Пластик', 'Тип': 'Ободковая', 'Цвет оправы': 'Синий', 'Форма': 'Круглые', 'Бренд': 'Tommy Hilfiger'}},
                    {'title': 'Betty Boop 07', 'id': 2, 'image': 'images/sun_1.jpg', 'price': 2200, 'status': 'в наличии', 'type': 'sunglasses', 'params': {'Пол': 'Детские', 'Материал': 'Пластик', 'Тип': 'Ободковая', 'Цвет оправы': 'Бордовый', 'Форма': 'Овальные', 'Бренд': 'Betty Boop'}},
                    {'title': 'Оправа для очков JIMMY CHOO JC230 EYR', 'id': 3, 'image': 'images/frame_2.jpg', 'price': 15300, 'status': 'в наличии', 'type': 'frames', 'params': {'Пол': 'Женские', 'Материал': 'Металл', 'Тип': 'Ободковая', 'Цвет оправы': 'Коричневый', 'Форма': 'Круглые', 'Бренд': 'Jimmy Choo'}}
                ]}, {
                'id': 2,
                'row': [
                    {'title': 'Детские солнцезащитные очки SAM-100', 'id': 4, 'image': 'images/sun_3.jpg', 'price': 2500, 'status': 'раскупили', 'type': 'sunglasses', 'params': {'Пол': 'Детские', 'Материал': 'Пластик', 'Тип': 'Ободковая', 'Цвет оправы': 'Серый', 'Форма': 'Прямоугольные', 'Бренд': 'Action Man'}},
                    {'title': 'Солнцезащитные детские очки Barbie SB — 157', 'id': 5, 'image': 'images/sun_4.jpg', 'price': 8500, 'status': 'в наличии', 'type': 'sunglasses', 'params': {'Пол': 'Детские', 'Материал': 'Металл', 'Тип': 'Ободковая', 'Цвет оправы': 'Розовый', 'Форма': 'Овальные', 'Бренд': 'Barbie'}},
                    {'title': 'Оправа для очков Polaroid PLD D346 I21', 'id': 6, 'image': 'images/frame_3.jpg', 'price': 13900, 'status': 'в наличии', 'type': 'frames', 'params': {'Пол': 'Мужские', 'Материал': 'Пластик', 'Тип': 'Ободковая', 'Цвет оправы': 'Чёрный', 'Форма': 'Квадратные', 'Бренд': 'Polaroid'}},
                ]}, {
                'id': 3,
                'row': [
                    {'title': 'Контактные линзы Adria 1 tone lavender 3 мес. (2 линзы)', 'id': 7, 'image': 'images/lense_1.jpg', 'price': 1350, 'status': 'в наличии', 'type': 'lenses', 'params': {'Частота замены': 'На 3 месяца', 'Бренд': 'Adria'}},
                    {'title': 'Оправа для очков TOMMY HILFIGER TH 1787 0VK', 'id': 8, 'image': 'images/frame_4.jpg', 'price': 8500, 'status': 'в наличии', 'type': 'frames', 'params': {'Пол': 'Мужские', 'Материал': 'Пластик', 'Тип': 'Ободковая', 'Цвет оправы': 'Чёрный', 'Форма': 'Круглые', 'Бренд': 'Tommy Hilfiger'}},
                    {'title': 'Betty Boop 19', 'id': 9, 'image': 'images/sun_2.jpg', 'price': 2200, 'status': 'в наличии', 'type': 'sunglasses', 'params': {'Пол': 'Детские', 'Материал': 'Металл', 'Тип': 'Ободковая', 'Цвет оправы': 'Коричневый', 'Форма': 'Овальные', 'Бренд': 'Betty Boop'}}
                ]}
        ],
        'priceMin': 1350,
        'priceMax': 15300,
        'priceMinAbsolute': 1350,
        'priceMaxAbsolute': 15300,
        'types': [{'id': 1, 'name': 'Оправы для очков', 'engName': 'frames', 'active': False}, {'id': 2, 'name': 'Солнцезащитные очки', 'engName': 'sunglasses', 'active': False}, {'id': 3, 'name': 'Контактные линзы', 'engName': 'lenses', 'active': False}]
    }}

data = getDatabase()

def updatePrices():
    priceMinAbsolute = 999999999
    priceMaxAbsolute = 0
    cnt = 0
    for row in data['data']['products']:
        for product in row['row']:
            cnt += 1
            if product['price'] < priceMinAbsolute:
                priceMinAbsolute = product['price']
            if product['price'] > priceMaxAbsolute:
                priceMaxAbsolute = product['price']
    if cnt != 0:
        data['data']['priceMin'] = priceMinAbsolute
        data['data']['priceMax'] = priceMaxAbsolute
        data['data']['priceMinAbsolute'] = priceMinAbsolute
        data['data']['priceMaxAbsolute'] = priceMaxAbsolute

def GetProducts(request):
    filterType('all')
    return render(request, 'products.html', data)

def GetProduct(request, id):
    DATABASE = getDatabase()
    res_data = {}
    for row in DATABASE['data']['products']:
        for product in row['row']:
            if product['id'] == id:
                res_data = product
    params = []
    for key in res_data['params'].keys():
        params.append({
            'key': key,
            'value': res_data['params'][key]
        })
    return render(request, 'product.html', {'data' : {
        'id': id,
        'product': res_data,
        'types': DATABASE['data']['types'],
        'params': params
    }})

def filterType(engName):
    global data
    data = getDatabase()
    if engName == 'all':
        return
    data['data']['products'] = []
    for type in data['data']['types']:
        if type['engName'] == engName:
            type['active'] = True
        else:
            type['active'] = False
    curr_id = 0
    cnt = 3
    for row in getDatabase()['data']['products']:
        for product in row['row']:
            if product['type'] == engName:
                cnt += 1
                if cnt > 3:
                    cnt -= 3
                    curr_id += 1
                    data['data']['products'].append({'id': curr_id, 'row': []})
                data['data']['products'][-1]['row'].append(product)
    updatePrices()

def filterPrice(priceMin, priceMax):
    oldproducts = data['data']['products']
    data['data']['products'] = []
    curr_id = 0
    cnt = 3
    for row in oldproducts:
        for product in row['row']:
            if product['price'] >= priceMin and product['price'] <= priceMax:
                cnt += 1
                if cnt > 3:
                    cnt -= 3
                    curr_id += 1
                    data['data']['products'].append({'id': curr_id, 'row': []})
                data['data']['products'][-1]['row'].append(product)
    updatePrices()
    data['data']['priceMin'] = priceMin
    data['data']['priceMax'] = priceMax

def GetType(request, engName):
    filterType(engName)
    return render(request, 'products.html', data)

def filter(request, engName='all'):
    if (engName == 'all'):
        filterType(engName)
    try:
        priceMin = int(request.GET['price_min'])
    except:
        priceMin = data['data']['priceMinAbsolute']
    try:
        priceMax = int(request.GET['price_max'])
    except:
        priceMax = data['data']['priceMaxAbsolute']
    filterPrice(priceMin, priceMax)
    return render(request, 'products.html', data)

