from django.urls import path
from . import views

urlpatterns = [
    path('place_order/<int:flower_id>/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/success/', views.order_success, name='order_success'),
]
