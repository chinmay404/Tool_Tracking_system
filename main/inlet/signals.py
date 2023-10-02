# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Master,ProductIndex



# @receiver(post_save, sender=ProductIndex)
# def add_products_to_master(sender, instance, **kwargs):
#     if instance.quantity_received > 0:
#         for _ in range(instance.quantity_received):
#             Master.objects.create(product=instance.product)
