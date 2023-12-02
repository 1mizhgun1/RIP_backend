from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

import redis
from BACKEND.settings import REDIS_HOST, REDIS_PORT

from ..models import *
from ..serializers import *
from ..services import *


session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


class Link_View(APIView):
    # изменение количества продукта в заказе
    # можно только если авторизован
    @swagger_auto_schema(request_body=OrdersItemsSerializer)
    def put(self, request, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try: 
            cnt = request.data['product_cnt']
            productId = request.data['product']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if OpticItem.objects.get(pk=productId).cnt < cnt:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        links = OrdersItems.objects.filter(product=productId).filter(order_id=getOrderID(request))
        if len(links) > 0:
            links[0].product_cnt = cnt
            links[0].save()
            return Response(PositionSerializer(links[0]).data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # удаление продукта из заказа
    # можно только если авторизован
    @swagger_auto_schema(request_body=OrdersItemsSerializer)
    def delete(self, request, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try: 
            productId = request.data['product']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        orderID = getOrderID(request)
        links = OrdersItems.objects.filter(product=productId).filter(order_id=orderID)
        if len(links) > 0:
            links[0].delete()
            if len(OrdersItems.objects.filter(order_id=orderID)) == 0:
                OpticOrder.objects.get(pk=orderID).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)