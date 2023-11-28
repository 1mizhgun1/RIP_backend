from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

import redis
from BACKEND.settings import REDIS_HOST, REDIS_PORT

from ..models import *
from ..serializers import *


session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


class Link_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # изменение количества продукта в заказе
    # можно только если авторизован
    @swagger_auto_schema(request_body=OrdersItemsSerializer)
    def put(self, request, format=None):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        try: 
            cnt = request.data['product_cnt']
            productId = request.data['product']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if OpticItem.objects.get(pk=productId).cnt < cnt:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        links = OrdersItems.objects.filter(product=productId).filter(order=User.objects.get(pk=currentUser.pk).active_order)
        if len(links) > 0:
            links[0].product_cnt = cnt
            links[0].save()
            return Response(PositionSerializer(links[0]).data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # удаление продукта из заказа
    # можно только если авторизован
    @swagger_auto_schema(request_body=OrdersItemsSerializer)
    def delete(self, request, format=None):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        try: 
            productId = request.data['product']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        links = OrdersItems.objects.filter(product=productId).filter(order=currentUser.active_order)
        if len(links) > 0:
            links[0].delete()
            if len(OrdersItems.objects.filter(order=currentUser.active_order)) == 0:
                OpticOrder.objects.get(pk=currentUser.active_order).delete()
                currentUser.active_order = -1
                currentUser.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)