# Generated by Django 4.2.6 on 2023-11-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_orderitem_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now=True, default='', verbose_name='Commande complète'),
            preserve_default=False,
        ),
    ]
