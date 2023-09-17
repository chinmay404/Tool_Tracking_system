
from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_check ,name='user_checking'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('user_check/', views.user_check, name='user_check'),
    path('logout/', views.logout_view, name='logout'),
]
