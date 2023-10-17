from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('',views.outlet_home,name='outlet_home'),
    path('creat_saleorder/',views.create_sale_order,name='creat_saleorder'),
    path('sale-orders/<int:sale_order_id>/', views.sale_order_detail, name='sale_order_detail'),
]