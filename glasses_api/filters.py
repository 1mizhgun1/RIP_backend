def filterStatus(queryset, request):
    if request.query_params.get('status'):
        return queryset.filter(status=request.query_params.get('status'))
    return queryset

def filterType(queryset, request):
    if request.query_params.get('type'):
        return queryset.filter(type=request.query_params.get('type'))
    return queryset

def filterPrice(queryset, request):
    priceMin = 0
    priceMax = 10 ** 10
    if request.query_params.get('price_min'):
        priceMin = request.query_params.get('price_min')
    if request.query_params.get('price_max'):
        priceMax = request.query_params.get('price_max')
    return queryset.filter(price__range=[priceMin, priceMax])

def filterUser(queryset, request):
    if request.query_params.get('user'):
        return queryset.filter(user=request.query_params.get('user'))
    return queryset

def filterModerator(queryset, request):
    if request.query_params.get('moderator'):
        return queryset.filter(moderator=request.query_params.get('moderator'))
    return queryset

def filterProducts(queryset, request):
    return filterPrice(filterType(filterStatus(queryset, request), request), request)

def filterOrders(queryset, request):
    return filterModerator(filterUser(filterStatus(queryset, request), request), request)