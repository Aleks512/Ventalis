from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('store/', views.store, name="store"),

	path('produits/',views.products, name="products"),
	path('products/list/manage/', views.products_list_mng, name='products-list-mng'),
	path('product/create/', views.product_create_view, name='product-create'),
	path('product/<slug:slug>/update/', views.product_update_view, name='product-update'),
	path('product/<slug:slug>/delete/', views.product_delete_view, name='product-delete'),

]