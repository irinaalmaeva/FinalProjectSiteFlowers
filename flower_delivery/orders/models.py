from django.db import models
from django.contrib.auth.models import User
from flowers.models import Flower  # Импорт модели Flower из приложения flowers

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В процессе'),
        ('delivered', 'Доставлен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    flowers = models.ManyToManyField(Flower, verbose_name='Цветы')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')

    def __str__(self):
        flowers_names = ", ".join([flower.name for flower in self.flowers.all()])  # Получаем названия всех цветков
        return f'Заказ №{self.id} - {flowers_names}'






