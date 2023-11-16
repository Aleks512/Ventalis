import asyncio
import datetime
from datetime import timezone
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pprint import pprint

from django.views.decorators.http import require_POST
from django.views.generic import DeleteView

from users.models import Address
from .forms import ProductCreateForm, ProductUpdateForm, ProductDeleteForm, AddressForm
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
    order_item, created = OrderItem.objects.get_or_create(customer=request.user.customer,order=order, product=product, ordered=False)

    # Mettre à jour la quantité et envoyer un message approprié
    if created:
        messages.success(request, "Produit ajouté au panier avec succès.")
    else:
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "La quantité du produit a été mise à jour.")

    # Rediriger vers la page des produits
    return redirect('products')


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = "store/order_item_delete.html"
    fields = '__all__'
    def get_success_url(self):
        return '/cart'



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

@login_required()
def checkout(request):
    if request.user:
        customer = request.user.customer
        # # Vérifier si une commande non complétée existe déjà pour le client
        # order = Order.objects.filter(customer=customer, completed=False).first()

        # Si aucune commande n'existe, créer une nouvelle commande
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = OrderItem.objects.filter(order=order)
        # Check if the user has an existing address
        user_addresses = Address.objects.filter(user=customer)
        existing_address = None
        if user_addresses.exists():
            existing_address = user_addresses.first()
        if request.method == 'POST':
            address_form = AddressForm(request.POST, instance=existing_address)
            if address_form.is_valid():
                address_instance = address_form.save(commit=False)
                address_instance.user = customer
                address_instance.order = order
                address_instance.address_type = 'S'
                address_instance.default = True
                address_instance.save()
                print(address_form.has_changed())
                print(address_form.is_bound)
                # Continue with your checkout logic here
                return redirect('checkout')  # Redirect to the checkout page or another page
        else:
            address_form = AddressForm()

        cartItems = order.get_cart_items()
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'address_form': address_form, 'existing_address': existing_address}
        return render(request, 'store/checkout.html', context)
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")

# Fonction de vérification pour s'assurer que l'utilisateur est un consultant$



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
    return redirect('products-list-mng')


@require_POST
def update_cart_item_quantity(request, item_id, action):
    item = get_object_or_404(OrderItem, id=item_id)

    if action == 'increment':
        item.quantity += 1
    elif action == 'decrement':
        if item.quantity > 1000:
            item.quantity -= 1
    item.save()

    cart_total = item.order.get_cart_total()  # Update the cart's total
    cart_items = item.order.get_cart_items()  # Update the total number of items in the cart

    return JsonResponse({
        'quantity': item.quantity,
        'total': item.get_total,  # Pass the property directly
        'cart_total': cart_total,
        'cart_items': cart_items,
    })

@login_required
def edit_address(request, address_id):
    address = Address.objects.get(pk=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('checkout')  # Redirigez l'utilisateur vers la page de profil ou une autre page
    else:
        form = AddressForm(instance=address)

    return render(request, 'store/edit_address.html', {'form': form})


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        # Vérifier si une commande non complétée existe déjà pour le client
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        order.transactionId=transaction_id
        order.completed = True
        order.save()
        # Set the status of each OrderItem to 'En traitement'
        items = order.orderitem_set.all()
        for item in items:
            item.status = OrderItem.Status.PROCESSING
            item.ordered = True
            item.save()
        # Perform any other necessary actions related to processing the order
    messages.success(request, 'Votre commande a été passée avec succès. Merci!')
    # Redirect to the 'products' page or wherever you want to redirect after processing the order
    return redirect('products')

# @login_required()
# def process_payment(request):
#     # Ici, vous pouvez intégrer le traitement du paiement avec votre passerelle de paiement
#     # Dans cet exemple, nous simulons un paiement réussi
#     # Assurez-vous d'ajouter une logique appropriée pour le traitement des paiements réels
#     order_id = request.GET.get('order_id')
#     order = Order.objects.get(id=order_id)
#
#     # Marquez la commande comme complète
#     order.completed = True
#     order.save()
#
#     return HttpResponse("Paiement réussi !")

