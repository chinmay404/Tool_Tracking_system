from django.contrib import admin
from .models import Product, ProductIndex, Master


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_id', 'supplier_name', 'description')
    search_fields = ('name', 'supplier_name')


@admin.register(ProductIndex)
class ProductIndexAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_requested',
                    'quantity_received', 'arrive_date','received_by','batch_id')
    list_filter = ('arrive_date',)
    search_fields = ('product__name','batch_id')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('product', 'uuid', 'added_date','received_by', 'status','batch_id')
    list_filter = ('status','added_date')
    search_fields = ('product__name', 'uuid','batch_id')


# Register your models with the admin site
# admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductIndex, ProductIndexAdmin)
# admin.site.register(Master, MasterAdmin)
