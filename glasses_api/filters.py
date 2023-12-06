def filterStatus(queryset, request):
    if request.GET.get('status'):
        return queryset.filter(status=request.GET.get('status'))
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


def filterProducts(queryset, request):
    return filterTitle(filterPrice(filterStatus(queryset, request), request), request)


def filterOrderStatus(queryset, request):
    if request.GET.get('status'):
        return queryset.filter(status__in=list(request.GET.get('status')))
    return queryset


def filterOrders(queryset, request):
    return filterOrderStatus(queryset, request)