from django.contrib import admin
from django.urls import path

from laba_1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.GetFilteredProducts, name='base_url'),
    path('products/<int:id>/', views.GetProduct, name='product_url')
]