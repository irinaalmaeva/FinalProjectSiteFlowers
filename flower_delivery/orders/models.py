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
    status = models.CharField(max_length=20, choices=[('new', 'Новый'), ('in_progress', 'В процессе'), ('delivered', 'Доставлен')], default='new', verbose_name='Статус')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return f'Заказ №{self.id} - {self.flower.name}'


