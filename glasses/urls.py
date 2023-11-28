from django.contrib import admin
from django.urls import path

from laba_1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'', GetProducts, name='base_url'),
    path(r'products/<int:id>/', GetProduct, name='product_url'),
]
