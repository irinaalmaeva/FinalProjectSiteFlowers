from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=100)  # Название цветка
    description = models.TextField(blank=True)  # Описание цветка
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена цветка
    image = models.ImageField(upload_to='flowers/', blank=True, null=True)  # Изображение цветка
    created_at = models.DateTimeField(auto_now_add=True)  # Дата добавления цветка

    def __str__(self):
        return self.name



