from django.db import models
from inlet.models import Product
from django.urls import reverse

class SaleOrderProduct(models.Model):
    sale_order = models.ForeignKey('SaleOrder', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    grn_number = models.CharField(max_length=50)
    po_number = models.CharField(max_length=50)
    bill_no = models.CharField(max_length=50)
    vehicle_no = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through=SaleOrderProduct)

    def total_quantity(self):
        return sum(item.quantity for item in self.saleorderproduct_set.all())
