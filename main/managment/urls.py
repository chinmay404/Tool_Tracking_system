
from django.urls import path
from . import views




urlpatterns = [
    # path('', views.user_check ,name='user_checking'),
    path('', views.home, name='managment_home_black'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='managment_home'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_only/', views.admin_only, name='admin_only'),
    path('wating_feild/', views.wating_feild, name='wating_feild'),
    path('inquiry/', views.inquiry, name='inquiry'),
    
]
