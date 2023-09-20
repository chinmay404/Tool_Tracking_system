from django.urls import path
from . import views
from django.views.generic import RedirectView


app_name = 'inlet'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='inlet_home', permanent=False)),
    path('home/', views.home, name='inlet_home'),
    path('create_product_index/',views.create_product_index,name='create_product_index'),
    path('list_product_index/', views.list_product_index,name='list_product_index'),
    path('list_masters/', views.list_masters, name='list_masters'),
]
