from django.db import models
import uuid
from managment.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

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


@receiver(post_save, sender=ProductIndex)
def add_products_to_master(sender, instance, **kwargs):
    if instance.quantity_received > 0:
        for _ in range(instance.quantity_received):
            Master.objects.create(product=instance.product)


class Master(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactive', 'Deactive'),
        ('in_progress', 'In Progress'),
        ('dead', 'Dead'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='deactive')
    added_date = models.DateField(auto_now_add=True)
    received_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, editable=False)  
    data_json = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.product.name} ({self.uuid})"


