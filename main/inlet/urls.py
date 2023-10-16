from django.urls import path,include
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='inlet_home', permanent=False)),
    path('home/', views.home, name='inlet_home'),
    path('create_product_index/',views.create_product_index,name='create_product_index'),
    path('list_product_index/', views.list_product_index,name='list_product_index'),
    path('list_masters/', views.list_masters, name='list_masters'),
    path('product_specification/<int:product_id>/', views.product_specification, name='product_specification'),
    path('product_batch/<uuid:batch_id>/', views.product_batch, name='product_batch'),
    path('product_quantity/<int:product_id>/', views.product_quantity, name='product_quantity'),
    # path('download_ids/<uuid:batch_id>/', views.download_ids, name='download_ids'),
    # path('download_id/<uuid:master_id>/', views.download_id, name='download_id'),
    path('api/', include('api.urls')),
    path('view_product/<str:product_id>/', views.view_master, name='view_product'),

]
