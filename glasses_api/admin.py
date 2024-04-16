from django.contrib import admin

from .models import *

admin.site.register(OpticItem)
admin.site.register(User)
admin.site.register(OpticOrder)
admin.site.register(OrdersItems)