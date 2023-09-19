from django.db import models
import uuid
from managment.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=100)
    product_id = models.PositiveIntegerField()
    supplier_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductIndex(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField()
    received_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    arrive_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Index"


class Master(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactive', 'Deactive'),
        ('in_progress', 'In Progress'),
        ('dead', 'Dead'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    added_date = models.DateField(auto_now_add=True)
    received_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='deactive')

    def __str__(self):
        return f"{self.product.name} ({self.uuid})"
