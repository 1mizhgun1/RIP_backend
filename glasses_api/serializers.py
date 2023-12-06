from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from collections import OrderedDict


class OpticItemSerializer(ModelSerializer):
    def get_fields(self):
        new_fields = OrderedDict()
        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field
        return new_fields

    class Meta:
        model = OpticItem
        fields = ["pk","title","file_extension","price","cnt","status","type","param_sex","param_material","param_type","param_color","param_form","param_time","param_brand","last_modified"]


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_moderator = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    is_active = serializers.BooleanField(default=True, required=False)
    
    class Meta:
        model = User
        fields = ["is_moderator","is_staff","is_superuser","is_active","username","password"]
        
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class OpticOrderSerializer(ModelSerializer):
    # username = serializers.SerializerMethodField()
    # modername = serializers.SerializerMethodField()
    
    def get_fields(self):
        new_fields = OrderedDict()
        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field
        return new_fields
    
    # def get_username(self, obj):
    #     print(obj.__fields__)
    #     return obj.user.username
    
    # def get_modername(self, obj):
    #     return obj.moderator.username

    class Meta:
        model = OpticOrder
        fields = ["pk","created","send","closed","status","user","moderator"]


class OrdersItemsSerializer(ModelSerializer):
    def get_fields(self):
        new_fields = OrderedDict()
        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field
        return new_fields

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
        fields = ["pk","title","price","cnt"]
