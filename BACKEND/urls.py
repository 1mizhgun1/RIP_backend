from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from glasses_api.views.OpticItemViews import *
from glasses_api.views.OpticOrderViews import *
from glasses_api.views.OrdersItemsViews import *
from glasses_api.views.UserViews import *
from glasses_api.views.PricesViews import *
from glasses_api.views.TypeViews import *

router = routers.DefaultRouter()

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path(r'products/', processOpticItemList, name='products-action'),       # GET, POST (title, file_extension, price, cnt, type, param_brand, image)
    path(r'products/<int:pk>/', processOpticItem, name='product-action'),   # GET, POST, PUT(title, file_extension, price, cnt, type, param_brand, image, additional params), DELETE (status)

    path(r'orders/', processOpticOrderList, name='orders-action'),      # GET, PUT, DELETE
    path(r'orders/<int:pk>/', processOpticOrder, name='order-action'),  # GET, PUT (user_id, moderator_id), DELETE (status)

    path(r'links/', processLink, name='link-action'),   # PUT (product, cnt), DELETE (product)

    path(r'users/', postUser, name='user-action'),  # POST (id_moderator, name, login, password)

    path(r'prices/', getPrices, name='get-prices'), # GET
    
    path(r'types/', getTypeList, name='get-types'), # GET
]