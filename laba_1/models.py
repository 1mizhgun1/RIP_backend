from django.db import models

class OpticItem(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    link = models.CharField(max_length=50, verbose_name="Ссылка на изображение")
    price = models.IntegerField(verbose_name="Цена")
    cnt = models.IntegerField(verbose_name="Количество на складе")
    status = models.CharField(max_length=1, verbose_name="Статус активности") # A - active, N - non-active
    type = models.CharField(max_length=20, verbose_name="Тип")
    param_sex = models.CharField(max_length=10, verbose_name="Пол", null=True, blank=True)
    param_material = models.CharField(max_length=20, verbose_name="Материал", null=True, blank=True)
    param_type = models.CharField(max_length=20, verbose_name="Тип оправы", null=True, blank=True)
    param_color = models.CharField(max_length=20, verbose_name="Цвет оправы", null=True, blank=True)
    param_form = models.CharField(max_length=20, verbose_name="Форма", null=True, blank=True)
    param_time = models.CharField(max_length=20, verbose_name="Частота замены", null=True, blank=True)
    param_brand = models.CharField(max_length=50, verbose_name="Бренд")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение", null=True, blank=True)

class User(models.Model):
    is_moderator = models.BooleanField(verbose_name="Модератор?")
    name = models.CharField(max_length=20, verbose_name="Имя")
    login = models.CharField(max_length=20, verbose_name="Логин")
    password = models.CharField(max_length=50, verbose_name="Пароль")
    
class OpticOrder(models.Model):
    created = models.DateTimeField(auto_now=True, verbose_name="Создание")
    send = models.DateTimeField(verbose_name="Отправка", null=True, blank=True)
    closed = models.DateTimeField(verbose_name="Закрытие", null=True, blank=True)
    status = models.CharField(max_length=1, verbose_name="Статус") # I - inputing, P - processing, D - deleted by user, A - success, W - fail
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Пользователь", related_name="user")
    moderator = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Модератор", related_name="moderator")

# I-P-C
#  \D\W 

class OrdersItems(models.Model):
    product_cnt = models.IntegerField(verbose_name="Количество данного товара в данном заказе")
    order = models.ForeignKey(OpticOrder, on_delete = models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(OpticItem, on_delete = models.CASCADE, verbose_name="Товар")

    class Meta:
        unique_together = (('order', 'product'),)