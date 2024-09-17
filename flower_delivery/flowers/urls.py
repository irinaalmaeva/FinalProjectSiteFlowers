from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_catalog, name='flower_catalog'),
    path('checkout/', views.checkout, name='checkout'),
    path('flower_detail/<int:pk>/', views.flower_detail, name='flower_detail'),

]

