from django.db import models
import uuid
from uuid import uuid4
from managment.models import CustomUser
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.db.models import Count, F
from django.db.models.signals import pre_save


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
    # GRN_NO = models.CharField(max_length=255 , null=True)
    # GRN_NO = models.CharField(max_length=20)

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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True ,primary_key=True)
    batch_id=models.CharField(max_length=255,editable=False) 
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress')
    added_date = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    data_json = models.JSONField(default=dict,null=True)

    def __str__(self):
        return f"{self.product.name} ({self.uuid})"

@receiver(post_save, sender=ProductIndex)
def add_products_to_master(sender, instance, **kwargs):
    if instance.quantity_received > 0:
        received_by = instance.received_by
        batch_id = instance.batch_id
        master_instances = []
        # product_data = instance.product.get_product_data()
        for _ in range(instance.quantity_received):
            master_data = {
                'productindex_data': {
                    'batch_id': str(instance.batch_id),
                    'quantity_requested': instance.quantity_requested,
                    'quantity_received': instance.quantity_received,
                    'received_by': str(received_by),
                    'arrive_date': instance.arrive_date.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
            master_instances.append(Master(
                product=instance.product,
                received_by=received_by,
                batch_id=batch_id,
                data_json = master_data
            ))
        Master.objects.bulk_create(master_instances)


# @receiver(post_save, sender=ProductIndex)
# def add_products_to_master(sender, instance, **kwargs):
#     if instance.quantity_received > 0:
#         for _ in range(instance.quantity_received):
#             Master.objects.create(product=instance.product)


@receiver(pre_save, sender=Master)
def update_product_index_status(sender, instance, **kwargs):
    if instance.status == 'active':
        active_masters_count = Master.objects.filter(product=instance.product, status='active').count()
        total_masters_count = Master.objects.filter(product=instance.product).count()
        if active_masters_count == total_masters_count:
            ProductIndex.objects.filter(product=instance.product).update(status='active')