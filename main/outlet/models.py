from django.db import models
from inlet.models import Product,Master
from django.urls import reverse

class SaleOrderProduct(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complet', 'Complete'),
    ]
    
    sale_order = models.ForeignKey('SaleOrder', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    uuids = models.JSONField(default=list, null=True, blank=True)


class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complet', 'Complete'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    grn_number = models.CharField(max_length=50)
    po_number = models.CharField(max_length=50)
    bill_no = models.CharField(max_length=50,primary_key=True)
    vehicle_no = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through=SaleOrderProduct)
    uuids = models.JSONField(default=list, null=True, blank=True)

    def total_quantity(self):
        return sum(item.quantity for item in self.saleorderproduct_set.all())
    
    def save(self, *args, **kwargs):
        if self.saleorderproduct_set.exists() and all(product.status == 'complete' for product in self.saleorderproduct_set.all()):
            self.status = 'complete'
        else:
            self.status = 'pending'

        super(SaleOrder, self).save(*args, **kwargs)


