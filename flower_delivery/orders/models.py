from django.db import models
from django.contrib.auth.models import User
from flowers.models import Flower  # Импорт модели Flower из приложения flowers

class OrderStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    flowers = models.ManyToManyField(Flower, verbose_name='Цветы')
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, verbose_name='Статус')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"

