from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_catalog, name='flower_catalog'),
    path('place_order/<int:flower_id>/', views.place_order, name='place_order'),
    path('flower_detail/<int:pk>/', views.flower_detail, name='flower_detail'),

    # Новый маршрут для добавления товара в корзину
    path('add_to_cart/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),

    # Новый маршрут для просмотра корзины
    path('cart/', views.view_cart, name='view_cart'),
]
