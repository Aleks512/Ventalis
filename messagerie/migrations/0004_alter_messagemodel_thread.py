# Generated by Django 4.2.6 on 2023-11-01 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messagerie', '0003_rename_sender_threadmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='thread',
            field=models.ForeignKey(default='nn', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='messagerie.threadmodel'),
            preserve_default=False,
        ),
    ]