# Generated by Django 4.2.5 on 2023-09-21 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inlet', '0005_alter_master_batch_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productindex',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('deactive', 'Deactive')], default='deactive', max_length=20),
        ),
    ]
