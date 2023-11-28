def filterStatus(queryset, request):
    if request.GET.get('status'):
        return queryset.filter(status=request.GET.get('status'))
    return queryset

def filterType(queryset, request):
    if request.GET.get('type'):
        return queryset.filter(type=request.GET.get('type'))
    return queryset

def filterPrice(queryset, request):
    priceMin = 0
    priceMax = 10 ** 10
    if request.GET.get('price_min'):
        priceMin = request.GET.get('price_min')
    if request.GET.get('price_max'):
        priceMax = request.GET.get('price_max')
    return queryset.filter(price__range=[priceMin, priceMax])

def filterTitle(queryset, request):
    if request.GET.get('title'):
        return queryset.filter(title__icontains=request.GET.get('title'))
    return queryset

def filterUser(queryset, request):
    if request.GET.get('user'):
        return queryset.filter(user=request.GET.get('user'))
    return queryset

def filterModerator(queryset, request):
    if request.GET.get('moderator'):
        return queryset.filter(moderator=request.GET.get('moderator'))
    return queryset

def filterProducts(queryset, request):
    return filterTitle(filterPrice(filterType(filterStatus(queryset, request), request), request), request)

def filterOrders(queryset, request):
    return filterModerator(filterUser(filterStatus(queryset, request), request), request)