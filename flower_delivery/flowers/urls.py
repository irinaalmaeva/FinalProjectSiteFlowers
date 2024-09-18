from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_catalog, name='flower_catalog'),
    path('place_order/<int:flower_id>/', views.place_order, name='place_order'),
    path('flower_detail/<int:pk>/', views.flower_detail, name='flower_detail'),
]
