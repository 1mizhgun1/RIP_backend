from django.shortcuts import render

from .models import OpticItem

from .data_processing.get_data import *
from .data_processing.filter_data import *

from django.db import connection

def DeleteFromProducts(request):
    id = -1
    if 'delete_card' in request.POST.keys():
        id = request.POST['delete_card']
    if id != -1:
        with connection.cursor() as cursor:
            cursor.execute("update laba_1_opticitem set status = 'N' where id = " + id)

def GetProducts(request):
    DeleteFromProducts(request)
    
    productList = OpticItem.objects.filter(status='A')
    return render(request, 'products.html', {
        'data': {
            'products': filterProducts(productList, request).order_by('last_modified'),
            # 'types': getTypeList(''),
            'prices': getPrices(productList, request)
        }
    })

def GetProduct(request, id):
    product = OpticItem.objects.get(pk=id)
    return render(request, 'product.html', {
        'data' : {
            'id': id,
            'product': product,
            # 'types': getTypeList(''),
            'params': getParams(product)
        }
    })

# <div class="head-bar">
#             {% for type in data.types %}
#                 {% if type.active %}
#                     <a href="{% url 'type_url' type.engName %}" class="head-bar-button-{{ type.id }}-active">{{ type.name }}</a>
#                 {% else %}
#                     <a href="{% url 'type_url' type.engName %}" class="head-bar-button-{{ type.id }}">{{ type.name }}</a>
#                 {% endif %}
#             {% endfor %}
#         </div>