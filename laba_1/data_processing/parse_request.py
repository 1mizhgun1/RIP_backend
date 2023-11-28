def parsePrices(request):
    priceMin = 0
    priceMax = 10 ** 10
    if 'price_min' in request.GET.keys():
        priceMinStr = request.GET['price_min']
        if priceMinStr != '':
            priceMin = int(priceMinStr)
    if 'price_max' in request.GET.keys():
        priceMaxStr = request.GET['price_max']
        if priceMaxStr != '':
            priceMax = int(priceMaxStr)
    return {
        'price_min': priceMin,
        'price_max': priceMax
    }