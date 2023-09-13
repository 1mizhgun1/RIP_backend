from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=50)
    image_path = models.CharField(max_length=50)
    price = models.IntegerField()
    cnt = models.IntegerField()
    product_type = models.CharField(max_length=50)
    param_sex = models.CharField(max_length=20)
    param_material = models.CharField(max_length=20)
    param_type = models.CharField(max_length=20)
    param_color = models.CharField(max_length=20)
    param_form = models.CharField(max_length=20)
    param_time = models.CharField(max_length=20)
    param_brand = models.CharField(max_length=50)
    
class Order(models.Model):
    order_date = models.DateField()
    order_time = models.TimeField()

class OrdersProducts:
    cnt = models.IntegerField()
    order_id = models.ForeignKey(Order, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete = models.CASCADE)