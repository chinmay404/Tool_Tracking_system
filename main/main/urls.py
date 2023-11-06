from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from managment import views as managment_views
from django.contrib import admin

admin.site.site_title = 'Tool Tracking ADMIN'
admin.site.site_header = 'ADMIN Portal'
# admin.site.index_title = 'Welcome to My site Researcher Portal'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', managment_views.logout_view, name='logout'),
    path('managment/', include('managment.urls')),
    path('inlet/', include('inlet.urls')),
    path('api/', include('api.urls')),
    path('outlet/', include('outlet.urls')),
    path('', RedirectView.as_view(pattern_name='managment_home', permanent=False)),  
]
