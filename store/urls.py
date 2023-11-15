from django.urls import path

from . import views
from .views import update_cart_item_quantity

urlpatterns = [
	#Leave as empty string for base url
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add-to-cart'),

	path('products/',views.products, name="products"),
	path('products-management/', views.products_list_mng, name='products-list-mng'),
	path('product-details/<slug:slug>/', views.product_detail, name='product'),
	path('product/create/', views.product_create_view, name='product-create'),
	path('product/<slug:slug>/update/', views.product_update_view, name='product-update'),
	path('product/<slug:slug>/delete/', views.product_delete_view, name='product-delete'),
	path('update_cart_item_quantity/<int:item_id>/<str:action>/', update_cart_item_quantity, name='update_cart_item_quantity'),
	path('order-item/<pk>/delete', views.OrderItemDeleteView.as_view(), name='order-item-delete'),
	path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),



]