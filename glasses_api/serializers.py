from .models import *
from rest_framework.serializers import ModelSerializer

class OpticItemSerializer(ModelSerializer):
    class Meta:
        model = OpticItem
        fields = ["pk","title","file_extension","price","cnt","status","type","param_sex","param_material","param_type","param_color","param_form","param_time","param_brand","last_modified"]

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["pk","is_moderator","name","login","password","active_order"]

class OpticOrderSerializer(ModelSerializer):
    class Meta:
        model = OpticOrder
        fields = ["pk","created","send","closed","status","user","moderator"]

class OrdersItemsSerializer(ModelSerializer):
    class Meta:
        model = OrdersItems
        fields = ["pk","product_cnt","order","product"]

class PositionSerializer(ModelSerializer):
    class Meta:
        model = OrdersItems
        fields = ["product_cnt","product"]

class ProductInOrderSerializer(ModelSerializer):
    class Meta:
        model = OpticItem
        fields = ["title","price"]
