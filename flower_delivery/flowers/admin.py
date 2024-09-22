from django.contrib import admin
from .models import Flower
from orders.models import Order

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'order_date', 'address')
    filter_horizontal = ('flowers',)  # Для удобного выбора цветов в заказе