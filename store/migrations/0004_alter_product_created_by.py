# Generated by Django 4.2.6 on 2023-11-05 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('store', '0003_order_comment_orderitem_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.consultant'),
        ),
    ]