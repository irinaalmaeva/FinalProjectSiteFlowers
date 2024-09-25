from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('place_order/<int:flower_id>/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/success/', views.order_success, name='order_success'),
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'), # Для отображения подробной информации о заказе
    path('api/create_order/', views.create_order, name='create_order'),  # а также для создания заказа
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

]
