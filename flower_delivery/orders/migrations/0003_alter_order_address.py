# Generated by Django 5.1 on 2024-09-18 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_status_order_address_delete_orderstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес доставки'),
        ),
    ]
