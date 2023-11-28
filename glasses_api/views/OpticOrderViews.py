from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from ..models import OpticItem, OpticOrder, OrdersItems, User
from ..serializers import OpticItemSerializer, OpticOrderSerializer, PositionSerializer, ProductInOrderSerializer
from ..filters import filterOrders

from django.shortcuts import get_object_or_404

from glasses_api.minio.MinioClass import MinioClass

from datetime import datetime

from .UserData import getUserId


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


@api_view(['Get', 'Put', 'Delete'])
def processOpticOrderList(request, format=None):

    # получение списка заказов
    if request.method == 'GET':
        orders = filterOrders(OpticOrder.objects.all(), request)
        serializer = OpticOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    # отправка заказа пользователем
    elif request.method == 'PUT':
        userId = getUserId()
        currentUser = User.objects.get(pk=userId)

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
    elif request.method == 'DELETE':
        userId = getUserId()
        currentUser = User.objects.get(pk=userId)
        
        order = get_object_or_404(OpticOrder, pk=currentUser.active_order)
        if checkStatusUpdate(order.status, "D", isModer=False):
            currentUser.active_order = -1
            currentUser.save()
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get', 'Put', 'Delete'])
def processOpticOrder(request, pk, format=None):

    # получение заказа
    if request.method == 'GET':
        order = get_object_or_404(OpticOrder, pk=pk)
        orderSerializer = OpticOrderSerializer(order)

        positions = OrdersItems.objects.filter(order=pk)
        positionsSerializer = PositionSerializer(positions, many=True)

        response = orderSerializer.data
        response['positions'] = getOrderPositionsWithProductData(positionsSerializer)

        return Response(response, status=status.HTTP_202_ACCEPTED)
    
    # изменение заказа
    elif request.method == 'PUT':
        order = get_object_or_404(OpticOrder, pk=pk)
        serializer = OpticOrderSerializer(order, data=request.data)
        if 'status' in request.data.keys():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # перевод заказа модератором на статус A или W
    elif request.method == 'DELETE':
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