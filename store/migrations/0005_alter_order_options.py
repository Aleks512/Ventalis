# Generated by Django 4.2.6 on 2023-11-16 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_orderitem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-date_ordered',)},
        ),
    ]