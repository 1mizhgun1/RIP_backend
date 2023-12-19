from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

import redis
from BACKEND.settings import REDIS_HOST, REDIS_PORT

from ..models import *
from ..serializers import *
from ..filters import *
from ..permissions import *
from ..services import *
from glasses_api.minio.MinioClass import MinioClass

from datetime import datetime
import requests


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
    # получение списка заказов
    # можно только если авторизован
    def get(self, request, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        username = session_storage.get(session_id)
        if username is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
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
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        order = get_object_or_404(OpticOrder, pk=getOrderID(request))
        new_status = "P"
        if checkStatusUpdate(order.status, new_status, isModer=False):
            url = "http://localhost:5000/pay/"
            params = {"order_id": order.pk}
            response = requests.post(url, json=params)
            
            order.status = new_status
            order.send = datetime.now()
            order.save()
            serializer = OpticOrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # удаление заказа пользователем
    # можно только если авторизован
    def delete(self, request, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        order = get_object_or_404(OpticOrder, pk=getOrderID(request))
        if checkStatusUpdate(order.status, "D", isModer=False):
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class OpticOrder_View(APIView):
    # получение заказа
    # можно получить свой заказ если авторизован
    # если авторизован и модератор, то можно получить любой заказ
    def get(self, request, pk, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        username = session_storage.get(session_id)
        if username is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
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
    @swagger_auto_schema(request_body=OpticOrderSerializer)
    def put(self, request, pk, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
        if not currentUser.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
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
    
    
class Cart_View(APIView):
    def get(self, request, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        username = session_storage.get(session_id)
        if username is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
        orders = OpticOrder.objects.filter(user=currentUser).filter(status='I')
        if orders.exists():
            order = orders.first()
            orderSerializer = OpticOrderSerializer(order)

            positions = OrdersItems.objects.filter(order=order.pk)
            positionsSerializer = PositionSerializer(positions, many=True)

            response = orderSerializer.data
            response['positions'] = getOrderPositionsWithProductData(positionsSerializer)

            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class OpticOrderStatus_View(APIView):
    # изменение статуса оплаты заказа
    # вызывается асинхронным сервисом
    @swagger_auto_schema(request_body=OpticOrderSerializer)
    def put(self, request, pk, format=None):
        payment_status = request.data["status"]
        try:
            order = OpticOrder.objects.get(pk=pk)
            order.payment = payment_status
            order.save()
            return Response(status=status.HTTP_200_OK)
        except OpticOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)