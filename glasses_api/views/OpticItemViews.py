from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes
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

import random


session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


# добавляет к сериализеру продукта поле image
def getProductDataWithImage(serializer: OpticOrderSerializer):
    minio = MinioClass()
    productData = serializer.data
    productData['image'] = minio.getImage('products', serializer.data['pk'], serializer.data['file_extension'])
    return productData


# выгружает картинку в minio из request
def postProductImage(request, serializer: OpticOrderSerializer):
    minio = MinioClass()
    minio.addImage('products', serializer.data['pk'], request.data['image'], serializer.data['file_extension'])


# изменяет картинку продукта в minio на переданную в request
def putProductImage(request, serializer: OpticOrderSerializer):
    minio = MinioClass()
    minio.removeImage('products', serializer.data['pk'], serializer.data['file_extension'])
    minio.addImage('products', serializer.data['pk'], request.data['image'], serializer.data['file_extension'])


class OpticItemList_View(APIView):
    # получение списка продуктов
    # можно всем
    def get(self, request, format=None):
        products = filterProducts(OpticItem.objects.all().order_by('last_modified'), request)

        data = {
            "order": getOrderID(request),
            "products": [getProductDataWithImage(OpticItemSerializer(product)) for product in products]
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)
    
    
    # добавление продукта
    # можно только если авторизован и модератор
    @method_permission_classes((IsModerator,))
    @swagger_auto_schema(request_body=OpticItemSerializer)
    def post(self, request, format=None):
        serializer = OpticItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            postProductImage(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class OpticItem_View(APIView):
    # получение продукта
    # можно всем
    def get(self, request, pk, format=None):
        product = get_object_or_404(OpticItem, pk=pk)
        serializer = OpticItemSerializer(product)
        return Response(getProductDataWithImage(serializer), status=status.HTTP_202_ACCEPTED)
    
    # добавление продукта в заказ
    # можно только если авторизован
    def post(self, request, pk, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
        orderID = getOrderID(request)
        if orderID == -1:   # если его нету
            order = {}      # то создаём черновик, заполняем нужные данные
            order['user'] = currentUser.pk
            order['moderator'] = random.choice(User.objects.filter(is_moderator=True)).pk
            orderSerializer = OpticOrderSerializer(data=order)
            if orderSerializer.is_valid():
                orderSerializer.save()  # сохраняем сериализер
                orderID = orderSerializer.data['pk']
                currentUser.save()
            else:
                return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # теперь у нас точно есть черновик, поэтому мы создаём связь м-м (не уверен что следующие две строки вообще нужны)    
        if OpticOrder.objects.get(pk=orderID).status != 'I' or len(OrdersItems.objects.filter(product=pk).filter(order=orderID)) != 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        link = {}
        link['product'] = pk
        link['order'] = orderID
        link['product_cnt'] = 1
        serializer = OrdersItemsSerializer(data=link)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # изменение продукта
    # можно только если авторизован и модератор
    @swagger_auto_schema(request_body=OpticItemSerializer)
    def put(self, request, pk, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
        if not currentUser.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        product = get_object_or_404(OpticItem, pk=pk)
        fields = request.data.keys()
        if 'pk' in fields or 'status' in fields or 'last_modified' in fields:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = OpticItemSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if 'image' in fields:
                putProductImage(request, serializer)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # логическое удаление/восстановление продукта
    # можно только если авторизован и модератор
    def delete(self, request, pk, format=None):
        session_id = get_session(request)
        if session_id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        currentUser = User.objects.get(username=session_storage.get(session_id).decode('utf-8'))
        if not currentUser.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        product = get_object_or_404(OpticItem, pk=pk)
        product.status = 'N' if product.status == 'A' else 'A'
        product.save()
        serializer = OpticItemSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)