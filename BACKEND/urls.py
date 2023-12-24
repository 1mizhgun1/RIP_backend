from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework import permissions

from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

from glasses_api.views.OpticItemViews import *
from glasses_api.views.OpticOrderViews import *
from glasses_api.views.OrdersItemsViews import *
from glasses_api.views.PricesViews import *

from glasses_api.views.AuthViews import *

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),

    path(r'products/', OpticItemList_View.as_view(), name='products-action'),       # GET, POST (title, file_extension, price, cnt, type, param_brand, image)
    path(r'products/<int:pk>/', OpticItem_View.as_view(), name='product-action'),   # GET, POST, PUT(title, file_extension, price, cnt, type, param_brand, image, additional params), DELETE

    path(r'orders/', OpticOrderList_View.as_view(), name='orders-action'),              # GET, PUT, DELETE
    path(r'orders/<int:pk>/', OpticOrder_View.as_view(), name='order-action'),          # GET, PUT (status)
    path(r'orders/<int:pk>/status/', OpticOrderStatus_View.as_view(), name='payment'),  # PUT

    path(r'links/', Link_View.as_view(), name='link-action'),   # PUT (product, cnt), DELETE (product)

    path(r'prices/', Prices_View.as_view(), name='get-prices'), # GETET
]