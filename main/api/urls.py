from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from django.urls import reverse
from .views import CreateOrder




urlpatterns = [
    path('get/product/<uuid:uuid>/', views.get_product, name='get_product'),  # Using 'get_product' as the name
    path('activate/product/<uuid:old_uuid>/<uuid:new_uuid>/', views.activate_product, name='activate_product'),
    path('', views.api_home, name='api_home'),
    path('batch_detail/<str:batch_id>/', views.batch_detail, name='batch_detail'),
    path('activate_master/<uuid:uuid>/', views.activate_master, name='activate_master'),
    # path('activate_master/<uuid:uuid>/', views.activate_master, name='activate_master'),
    path('post/creat_inlet/', CreateOrder.as_view(), name='creat_inlet'),
    
]
