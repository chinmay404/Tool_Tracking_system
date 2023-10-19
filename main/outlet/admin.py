from django.contrib import admin
from .models import SaleOrder, SaleOrderProduct
from .forms import SaleOrderForm

class SaleOrderProductInline(admin.TabularInline):
    model = SaleOrderProduct
    extra = 1  # You can adjust the number of SaleOrderProduct forms displayed

class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('grn_number', 'po_number', 'bill_no', 'vehicle_no')
    inlines = [SaleOrderProductInline]

    form = SaleOrderForm  # Use your custom form

admin.site.register(SaleOrder, SaleOrderAdmin)
