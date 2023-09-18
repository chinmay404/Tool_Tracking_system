from django.urls import path
from . import views



app_name = 'inlet'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home ,name='inlet_home'),
]
