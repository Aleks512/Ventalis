from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'price')
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id')
    list_filter = ('complete',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')


