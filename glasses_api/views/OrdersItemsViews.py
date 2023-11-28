from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from ..models import OpticItem, OpticOrder, OrdersItems, User
from ..serializers import PositionSerializer

from .UserData import getUserId

@api_view(['Put', 'Delete'])
def processLink(request, format=None):

    # изменение количества продукта в заказе
    if request.method == 'PUT':
        userId = getUserId()

        try: 
            cnt = request.data['cnt']
            productId = request.data['product']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if OpticItem.objects.get(pk=productId).cnt < cnt:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        links = OrdersItems.objects.filter(product=productId).filter(order=User.objects.get(pk=userId).active_order)
        if len(links) > 0:
            links[0].product_cnt = cnt
            links[0].save()
            return Response(PositionSerializer(links[0]).data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # удаление продукта из заказа
    elif request.method == 'DELETE':
        userId = getUserId()
        currentUser = User.objects.get(pk=userId)

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