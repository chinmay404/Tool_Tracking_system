from django.db import models
import uuid
from uuid import uuid4
from managment.models import CustomUser
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    product_id = models.PositiveIntegerField()
    supplier_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductIndex(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactive', 'Deactive'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='deactive')
    batch_id = models.UUIDField(default=uuid4, unique=True, editable=False) 
    quantity_requested = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField()
    received_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    arrive_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} Index"
    
    
    def update_batch_status(self):
        all_active = self.master_set.filter(status='active').count() == self.quantity_received
        self.status = 'active' if all_active else 'deactive'
        self.save()


class Master(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactive', 'Deactive'),
        ('in_progress', 'In Progress'),
        ('dead', 'Dead'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)

    batch_id=models.CharField(max_length=255,editable=False)  # Add this field

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress')
    added_date = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    data_json = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.product.name} ({self.uuid})"

@receiver(post_save, sender=ProductIndex)
def add_products_to_master(sender, instance, **kwargs):
    if instance.quantity_received > 0:
        received_by = instance.received_by
        batch_id = instance.batch_id
        master_instances = []
        for _ in range(instance.quantity_received):
            master_instances.append(Master(
                product=instance.product,
                received_by=received_by,
                batch_id=batch_id,
            ))
        Master.objects.bulk_create(master_instances)


# @receiver(post_save, sender=ProductIndex)
# def add_products_to_master(sender, instance, **kwargs):
#     if instance.quantity_received > 0:
#         for _ in range(instance.quantity_received):
#             Master.objects.create(product=instance.product)


