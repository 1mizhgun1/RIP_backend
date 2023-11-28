from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import OpticItem
from ..filters import filterProducts

from django.db.models import Min, Max


class Prices_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        orders = filterProducts(OpticItem.objects.all(), request)
        price_min = orders.aggregate(Min('price'))['price__min']
        price_max = orders.aggregate(Max('price'))['price__max']
        return Response({'price_min' : price_min, 'price_max': price_max}, status=status.HTTP_202_ACCEPTED)