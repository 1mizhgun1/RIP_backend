from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

import redis
from BACKEND.settings import REDIS_HOST, REDIS_PORT

from ..models import *
from ..serializers import *
from ..filters import filterOrders
from ..permissions import *
from glasses_api.minio.MinioClass import MinioClass

from datetime import datetime


session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


# проверяет, можно ли поменять статус заказа с old на new в зависимости от привилегий пользователя
def checkStatusUpdate(old, new, isModer):
    return ((not isModer) and (new in ['P', 'D']) and (old == 'I')) or (isModer and (new in ['A', 'W']) and (old == 'P'))


# добавляет картинку к позиции заказа
def getProductInOrderWithImage(serializer: ProductInOrderSerializer, pk: int, file_extension: str):
    minio = MinioClass()
    productData = serializer.data
    productData['image'] = minio.getImage('products', pk, file_extension)
    return productData


# добавляет данные продукта ко всем позициям заказа
def getOrderPositionsWithProductData(serializer: PositionSerializer):
    positions = []
    for item in serializer.data:
        product = get_object_or_404(OpticItem, pk=item['product'])
        positionData = item
        positionData['product_data'] = getProductInOrderWithImage(ProductInOrderSerializer(product), product.pk, product.file_extension)
        positions.append(positionData)
    return positions


class OpticOrderList_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # получение списка заказов
    # можно только если авторизован
    def get(self, request, format=None):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        if currentUser.is_moderator:
            orders = filterOrders(OpticOrder.objects.all(), request)
        else:
            orders = filterOrders(OpticOrder.objects.filter(user=currentUser), request)
        serializer = OpticOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    # отправка заказа пользователем
    # можно только если авторизован
    @swagger_auto_schema(request_body=OpticOrderSerializer)
    def put(self, request, format=None):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(ssid).decode('utf-8'))

        order = get_object_or_404(OpticOrder, pk=currentUser.active_order)
        new_status = "P"
        if checkStatusUpdate(order.status, new_status, isModer=False):
            currentUser.active_order = -1
            currentUser.save()
            order.status = new_status
            order.send = datetime.now()
            order.save()
            serializer = OpticOrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # удаление заказа пользователем
    # можно только если авторизован
    def delete(self, request, format=None):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        
        order = get_object_or_404(OpticOrder, pk=currentUser.active_order)
        if checkStatusUpdate(order.status, "D", isModer=False):
            currentUser.active_order = -1
            currentUser.save()
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class OpticOrder_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # получение заказа
    # можно получить свой заказ если авторизован
    # если авторизован и модератор, то можно получить любой заказ
    def get(self, request, pk, format=None):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        order_keys = OpticOrder.objects.filter(user=currentUser).values_list('pk', flat=True)
        if (pk in order_keys) or currentUser.is_moderator:
            order = get_object_or_404(OpticOrder, pk=pk)
            orderSerializer = OpticOrderSerializer(order)

            positions = OrdersItems.objects.filter(order=pk)
            positionsSerializer = PositionSerializer(positions, many=True)

            response = orderSerializer.data
            response['positions'] = getOrderPositionsWithProductData(positionsSerializer)

            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    
    # перевод заказа модератором на статус A или W
    # можно только если авторизован и модератор
    @method_permission_classes((IsModerator,))
    @swagger_auto_schema(request_body=OpticOrderSerializer)
    def put(self, request, pk, format=None):
        order = get_object_or_404(OpticOrder, pk=pk)
        try: 
            new_status = request.data['status']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if checkStatusUpdate(order.status, new_status, isModer=True):
            order.status = new_status
            order.closed = datetime.now()
            order.save()
            serializer = OpticOrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)