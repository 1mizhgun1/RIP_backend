from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from ..models import OpticItem, OpticOrder, OrdersItems, User
from ..serializers import OpticItemSerializer, OpticOrderSerializer, OrdersItemsSerializer
from ..filters import filterProducts

from django.shortcuts import get_object_or_404

from glasses_api.minio.MinioClass import MinioClass

import random

from .UserData import getUserId


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


@api_view(['Get', 'Post'])
def processOpticItemList(request, format=None):

    # получение списка продуктов
    if request.method == 'GET':
        products = filterProducts(OpticItem.objects.all().order_by('last_modified'), request)
        productsData = [getProductDataWithImage(OpticItemSerializer(product)) for product in products]
        return Response(productsData, status=status.HTTP_202_ACCEPTED)
    
    # добавление продукта
    elif request.method == 'POST':
        serializer = OpticItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            postProductImage(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get', 'Post', 'Put', 'Delete'])
def processOpticItem(request, pk, format=None):

    # получение продукта
    if request.method == 'GET':
        product = get_object_or_404(OpticItem, pk=pk)
        if request.method == 'GET':
            serializer = OpticItemSerializer(product)
            return Response(getProductDataWithImage(serializer), status=status.HTTP_202_ACCEPTED)
    
    # добавление продукта в заказ
    elif request.method == 'POST': # add to order
        userId = getUserId()
        currentUser = User.objects.get(pk=userId)
        orderId = currentUser.active_order # неважно каким образом, но вот здесь нам надо получить либо id черновика, либо узнать что его нету
        if orderId == -1:   # если его нету
            order = {}      # то создаём черновик, заполняем нужные данные
            order['user'] = userId
            order['moderator'] = random.choice(User.objects.filter(is_moderator=True)).pk
            orderSerializer = OpticOrderSerializer(data=order)
            if orderSerializer.is_valid():
                orderSerializer.save()  # сохраняем сериализер
                orderId = orderSerializer.data['pk']
                currentUser.active_order = orderId
                currentUser.save()
            else:
                return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # теперь у нас точно есть черновик, поэтому мы создаём связь м-м (не уверен что следующие две строки вообще нужны)    
        if OpticOrder.objects.get(pk=orderId).status != 'I' or len(OrdersItems.objects.filter(product=pk).filter(order=orderId)) != 0:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        link = {}
        link['product'] = pk
        link['order'] = orderId
        link['product_cnt'] = 1
        serializer = OrdersItemsSerializer(data=link)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # изменение продукта
    elif request.method == 'PUT':
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
    
    # логическое удаление/восстановление продуктаы
    elif request.method == 'DELETE':
        try: 
            new_status = request.data['status']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(OpticItem, pk=pk)
        product.status = new_status
        product.save()
        serializer = OpticItemSerializer(product)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)