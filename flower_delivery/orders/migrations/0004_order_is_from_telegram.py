# Generated by Django 5.1 on 2024-09-30 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_from_telegram',
            field=models.BooleanField(default=False, verbose_name='Заказ из Telegram'),
        ),
    ]
