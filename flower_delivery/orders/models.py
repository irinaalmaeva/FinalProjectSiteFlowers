from django.db import models
from django.contrib.auth.models import User  # Для связи с пользователем
from flowers.models import Flower

class OrderStatus(models.Model):
    name = models.CharField(max_length=50)  # Название статуса (например, 'В обработке', 'Доставлено')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Кто сделал заказ
    flowers = models.ManyToManyField(Flower, through='OrderItem')  # Связь с цветами через промежуточную таблицу
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)  # Статус заказа
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая сумма заказа
    created_at = models.DateTimeField(auto_now_add=True)  # Время заказа

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # К какому заказу относится
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)  # Какой цветок
    quantity = models.PositiveIntegerField(default=1)  # Количество цветов

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"
