from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('place_order/<int:flower_id>/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/success/', views.order_success, name='order_success'),
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Используем стандартное представление для входа,
]
