from django.utils.dateparse import parse_datetime


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


def filterOrderSend(queryset, request):
    start_date = parse_datetime("2000-01-01T00:00:00Z")
    end_date = parse_datetime("2100-01-01T00:00:00Z")
    if request.GET.get('start_date') and parse_datetime(request.GET.get('start_date')):
        start_date = parse_datetime(request.GET.get('start_date'))
    if request.GET.get('end_date') and parse_datetime(request.GET.get('end_date')):
        end_date = parse_datetime(request.GET.get('end_date'))
    return queryset.filter(send__range=[start_date, end_date])        


def filterOrders(queryset, request):
    return filterOrderSend(filterOrderStatus(queryset, request), request)