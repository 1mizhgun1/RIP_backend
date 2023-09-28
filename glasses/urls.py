from django.contrib import admin
from django.urls import path

from laba_1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetProducts, name='base_url'),
    path('products/<int:id>/', views.GetProduct, name='product_url'),
    path('filter', views.GetFilteredProducts),
    path('products/<str:engName>/', views.GetType, name='type_url'),
    path('products/<str:engName>/filter', views.GetFilteredProducts),
    path('delete', views.DeleteFromProducts),
    path('products/<str:engName>/delete', views.DeleteFromProducts)
]
