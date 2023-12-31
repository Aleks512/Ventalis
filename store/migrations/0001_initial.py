# Generated by Django 4.2.6 on 2023-11-27 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionId', models.CharField(blank=True, max_length=20, null=True)),
                ('date_ordered', models.DateTimeField(auto_now_add=True, verbose_name='Date de commande')),
                ('completed', models.BooleanField(default=False, verbose_name='Commande complète')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commantaire sur commande')),
            ],
            options={
                'ordering': ('-date_ordered',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'En attente'), ('PR', 'En traitement'), ('S', 'Expédié'), ('D', 'Livré'), ('R', 'Retourné')], default='P', max_length=2, verbose_name='Statut de la commande')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField(default=1000, verbose_name='Quantité')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commantaire sur articles')),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='OrderItemStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'En attente'), ('PR', 'En traitement'), ('S', 'Expédié'), ('D', 'Livré'), ('R', 'Retourné')], max_length=2, verbose_name='Nouveau statut de la commande')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commentaire sur la modification')),
                ('date_modified', models.DateTimeField(auto_now_add=True, verbose_name='Date de modification')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Prix')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='Catégorie')),
            ],
            options={
                'verbose_name': 'Produit',
                'verbose_name_plural': 'Produits',
                'ordering': ('-created_at',),
            },
        ),
    ]
