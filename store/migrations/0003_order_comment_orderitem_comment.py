# Generated by Django 4.2.6 on 2023-11-05 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_shippingaddress_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Commantaire sur commande'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Commantaire sur articles'),
        ),
    ]