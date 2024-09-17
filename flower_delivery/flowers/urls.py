from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_catalog, name='flower_catalog'),
    path('checkout/', views.checkout, name='checkout'),

]

