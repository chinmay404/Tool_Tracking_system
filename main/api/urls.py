from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views




urlpatterns = [
    path('get/product/<uuid:uuid>/', views.get_product, name='blank'),
    path('activate/product/<uuid:uuid>/', views.activate_product, name='activate_product'),
]