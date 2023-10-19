from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('',views.outlet_home,name='outlet_home'),
    path('creat_saleorder/',views.create_sale_order,name='creat_saleorder'),
    path('sale-orders/<int:bill_no>/', views.sale_order_detail, name='sale_order_detail'),
    path('add_uuid/<int:bill_no>/<int:sale_order_product_id>/', views.add_uuid, name='add_uuid'),
    path('sale-orders/<int:bill_no>/product/<int:sale_order_product_id>/', views.sale_order_product_detail, name='sale_order_product_detail'),
     path('sale-orders/<str:bill_no>/product/<int:sale_order_product_id>/save-and-return/', views.save_and_return, name='save_and_return'),
]