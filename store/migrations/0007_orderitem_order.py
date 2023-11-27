# Generated by Django 4.2.6 on 2023-11-10 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_complete_order_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='store.order', verbose_name='Commande'),
            preserve_default=False,
        ),
    ]