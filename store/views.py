import asyncio

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pprint import pprint


from .forms import ProductCreateForm, ProductUpdateForm, ProductDeleteForm
from .models import Category, Product, Order, OrderItem



def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')  # Récupérer la catégorie sélectionnée
    context = {"products": products, "categories": categories, "selected_category": selected_category}
    return render(request, "store/products.html", context)

def add_to_cart(request, slug):
    # Récupérer le produit en fonction du slug
    product = get_object_or_404(Product, slug=slug)

    # Récupérer ou créer le panier en cours pour l'utilisateur connecté
    order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)

    # Récupérer ou créer l'élément de commande pour le produit
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, ordered=False)

    # Mettre à jour la quantité et envoyer un message approprié
    if created:
        messages.success(request, "Produit ajouté au panier avec succès.")
    else:
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "La quantité du produit a été mise à jour.")

    # Rediriger vers la page des produits
    return redirect('products')


@login_required
def cart(request):
    if request.user.is_client:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        print(items)
        cartItems = order.get_cart_items()
        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'store/cart.html', context)
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")
@login_required
def checkout(request):
    if request.user.is_client:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        print(items)
        cartItems = order.get_cart_items()
        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'store/checkout.html', context)
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")

# Fonction de vérification pour s'assurer que l'utilisateur est un consultant
def is_consultant(user):
    return user.is_authenticated and user.is_employee

# Décorateur personnalisé pour les vues du CRUD des produits
def consultant_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not is_consultant(request.user):
            return redirect('login')  # Rediriger vers la page de connexion si l'utilisateur n'est pas un consultant
        return view_func(request, *args, **kwargs)
    return _wrapped_view
@consultant_required
def products_list_mng(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "store/products_list_mng.html", context={"products":products, "categories": categories})
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_cat = product.category
    related_products=product_cat.product_set.all()

    return render(request, "store/product_detail.html", context={"product":product, 'related_products':related_products})

@consultant_required
def product_create_view(request):
    form = ProductCreateForm(request.POST or None, request.FILES or None)
    categories = Category.objects.all()
    if form.is_valid():
        product = form.save(commit=False)
        product.created_by = request.user  # Déf l'utilisateur connecté comme créateur.
        product.save()
        return redirect('products-list-mng')
    return render(request, 'store/product_create.html', {'form': form,"categories": categories})

@consultant_required
def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products-list-mng')
    return render(request, 'store/product_update.html', {'form': form, 'product': product})

@consultant_required
def product_delete_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductDeleteForm(request.POST or None, instance=product)
    if request.method == 'POST':
        product.delete()
        return redirect('products-list-mng')
    return render(request, 'store/product_delete.html', {'form': form, 'product': product})


