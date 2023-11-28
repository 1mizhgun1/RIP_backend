"""
URL configuration for glasses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from laba_1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetProducts, name='base_url'),
    path('products/<int:id>/', views.GetProduct, name='product_url'),
    path('filter', views.filter),
    path('products/<str:engName>/', views.GetType, name='type_url'),
    path('products/<str:engName>/filter', views.filter),
]
