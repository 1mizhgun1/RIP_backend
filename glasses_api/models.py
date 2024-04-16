from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class NewUserManager(UserManager):
    def create_user(self, username, password, **extra_fields):
        user: User = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class OpticItem(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    file_extension = models.CharField(max_length=10, verbose_name="Расширение файла изображения")
    price = models.IntegerField(verbose_name="Цена")
    cnt = models.IntegerField(verbose_name="Количество на складе")
    status = models.CharField(max_length=1, verbose_name="Статус активности", default="A") # A - active, N - non-active
    type = models.CharField(max_length=10, verbose_name="Тип")
    param_sex = models.CharField(max_length=50, verbose_name="Пол", null=True, blank=True)
    param_material = models.CharField(max_length=50, verbose_name="Материал", null=True, blank=True)
    param_type = models.CharField(max_length=50, verbose_name="Тип оправы", null=True, blank=True)
    param_color = models.CharField(max_length=50, verbose_name="Цвет оправы", null=True, blank=True)
    param_form = models.CharField(max_length=50, verbose_name="Форма", null=True, blank=True)
    param_time = models.CharField(max_length=50, verbose_name="Частота замены", null=True, blank=True)
    param_brand = models.CharField(max_length=50, verbose_name="Бренд")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение", null=True, blank=True)
    
    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    objects = NewUserManager()

    username = models.CharField(max_length=32, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=256, verbose_name="Пароль") 
    is_moderator = models.BooleanField(verbose_name="Модератор?", default=False)
    is_staff = models.BooleanField(verbose_name="Можно в админку?", default=False)
    is_superuser = models.BooleanField(verbose_name="Суперсус?", default=False)
    is_active = models.BooleanField(verbose_name="Активный?", default=True)

    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username
    

class OpticOrder(models.Model):
    created = models.DateTimeField(auto_now=True, verbose_name="Создание")
    send = models.DateTimeField(verbose_name="Отправка", null=True, blank=True)
    closed = models.DateTimeField(verbose_name="Закрытие", null=True, blank=True)
    status = models.CharField(max_length=1, verbose_name="Статус", default='I') # I - inputing, P - processing, D - deleted by user, A - success, W - fail
    payment = models.CharField(max_length=1, verbose_name="Статус оплаты", default='N') # N - non-payed, A - success, W - fail
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Пользователь", related_name="user")
    moderator = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name="Модератор", related_name="moderator", null=True, blank=True)

# I --- P --- A
#  \     \
#   \     \
#    D     W
#
# I - created
# P - created, send
# D - created, send
# A - created, send, closed
# W - created, send, closed


class OrdersItems(models.Model):
    product_cnt = models.IntegerField(verbose_name="Количество данного товара в данном заказе")
    order = models.ForeignKey(OpticOrder, on_delete = models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(OpticItem, on_delete = models.CASCADE, verbose_name="Товар")

    class Meta:
        unique_together = (('order', 'product'),)