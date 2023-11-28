from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from ..models import OpticItem
from ..filters import filterProducts

from django.shortcuts import get_object_or_404

from django.db.models import Min, Max

@api_view(['Get'])
def getPrices(request, format=None):
    orders = filterProducts(OpticItem.objects.all(), request)
    price_min = orders.aggregate(Min('price'))['price__min']
    price_max = orders.aggregate(Max('price'))['price__max']
    return Response({'price_min' : price_min, 'price_max': price_max}, status=status.HTTP_202_ACCEPTED)