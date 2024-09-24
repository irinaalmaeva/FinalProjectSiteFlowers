from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_catalog, name='flower_catalog'),
    path('place_order/', views.place_order, name='place_order'),
    path('flower_detail/<int:pk>/', views.flower_detail, name='flower_detail'),

    # Новый маршрут для добавления товара в корзину
    path('add_to_cart/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),

    # Новый маршрут для просмотра корзины
    path('cart/', views.view_cart, name='view_cart'),
    # маршрут для удаления товара из корзины
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/flowers/', views.flower_catalog_api, name='flower_catalog_api'),
]
