from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    price = models.IntegerField()
    cnt = models.IntegerField()
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    param_sex = models.CharField(max_length=20)
    param_material = models.CharField(max_length=20)
    param_type = models.CharField(max_length=20)
    param_color = models.CharField(max_length=20)
    param_form = models.CharField(max_length=20)
    param_time = models.CharField(max_length=20)
    param_brand = models.CharField(max_length=50)

class User(models.Model):
    name = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=50)

class Moderator(models.Model):
    name = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    
class Order(models.Model):
    create = models.DateField()
    send = models.DateField()
    closed = models.DateField()
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    moderator = models.ForeignKey(Moderator, on_delete = models.CASCADE)

class OrdersProducts(models.Model):
    product_cnt = models.IntegerField()
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)