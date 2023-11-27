# Generated by Django 4.2.6 on 2023-11-12 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.CharField(default='', max_length=100, verbose_name='Street'),
            preserve_default=False,
        ),
    ]