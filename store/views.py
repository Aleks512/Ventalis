import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pprint import pprint
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, UpdateView, DetailView
from users.models import Address, Customer
from .forms import ProductCreateForm, ProductUpdateForm, ProductDeleteForm, AddressForm, OrderItemStatusForm, \
    CategoryForm
from .models import Category, Product, Order, OrderItem



def products(request):
    # Récupère tous les produits et catégories
    products = Product.objects.all()
    categories = Category.objects.all()

    # Récupérer le slug de la catégorie sélectionnée depuis l'URL
    selected_category_slug = request.GET.get('category')
    selected_category = None

    if selected_category_slug:
        # Récupère l'objet catégorie ou renvoie une erreur 404 si non trouvé
        selected_category = get_object_or_404(Category, slug=selected_category_slug)

        # Filtrer les produits en fonction de la catégorie sélectionnée
        products = products.filter(category=selected_category)
    else:
        # Si aucune catégorie n'est sélectionnée, tous les produits sont déjà sélectionnés
        pass

    # Préparer le contexte pour le template
    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category_slug  # Passer le slug au template
    }

    return render(request, "store/products.html", context)
@login_required()
def add_to_cart(request, slug):
    user = request.user

    if not user.is_authenticated:
        messages.warning(request, "Veuillez vous connecter pour ajouter des produits au panier.", extra_tags='not_logged_in')
        return redirect(reverse('login'))

    if user.is_superuser or user.is_employee:
        messages.warning(request, "Vous n'êtes pas autorisé à ajouter des produits au panier.", extra_tags='not_customer')
        #return redirect(reverse('home'))

    if not user.is_client:
        messages.info(request, "Vous êtes identifié, mais vous n'êtes pas un client. Vous pouvez continuer à naviguer.", extra_tags='not_customer')
        return redirect(reverse('product', kwargs={'slug': slug}))
    # Récupérer le produit en fonction du slug
    product = get_object_or_404(Product, slug=slug)

    # Récupérer la commande en cours pour l'utilisateur connecté
    order = Order.objects.filter(customer=request.user.customer, completed=False).first()

    # Si aucune commande n'existe, créer une nouvelle commande
    if not order:
        order = Order.objects.create(customer=request.user.customer)

    # Récupérer ou créer l'élément de commande pour le produit
    order_item, created = OrderItem.objects.get_or_create(customer=request.user.customer, order=order, product=product, ordered=False)

    # Mettre à jour la quantité et envoyer un message approprié
    if created:
        messages.success(request, "Produit ajouté au panier avec succès.")
    else:
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "La quantité du produit a été mise à jour.")

    # Rediriger vers la page des produits
    return redirect('products')

 # From cart delete OrderItem
class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = "store/order_item_delete.html"
    fields = '__all__'
    def get_success_url(self):
        return '/cart'



@login_required
def cart(request):

    if request.user.is_client: # Vérifier si l'utilisateur est un client
        customer = request.user.customer # Récupérer l'objet client
        order, created = Order.objects.get_or_create(customer=customer, completed=False) #
        items = order.orderitem_set.all() # # Récupérer tous les articles de commande pour la commande en cours
        cartItems = order.get_cart_items() # # Récupérer le nombre total d'articles dans le panier
        context = {'items': items, 'order': order, 'cartItems': cartItems} # Préparer le contexte pour le template
        return render(request, 'store/cart.html', context)
    else:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")

@login_required()
# Checkout view function to handle the checkout process
def checkout(request):
    # Vérifier si l'utilisateur est un client
    if request.user.is_client:
        customer = request.user.customer
        # Si aucune commande n'existe, créer une nouvelle commande
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = OrderItem.objects.filter(order=order) #
        # Check if the user has an existing address
        user_addresses = Address.objects.filter(user=customer) #
        existing_address = None # Initialize the existing address variable
        if user_addresses.exists(): # Check if the user has any addresses
            existing_address = user_addresses.first() # Get the first address
        if request.method == 'POST': # Check if the request method is POST
            address_form = AddressForm(request.POST, instance=existing_address)  # Create a new AddressForm instance
            if address_form.is_valid(): #  "address_form.is_valid()" vérifie si les données soumises sont valides
                address_instance = address_form.save(commit=False)  # Save the form data to the database
                address_instance.user = customer # Set the user for the address
                address_instance.order = order # Set the order for the address
                address_instance.address_type = 'S' # Set the address type to 'Shipping'
                address_instance.default = True # Set the address as the default shipping address
                address_instance.save() # Save the address instance
                # Continue with your checkout logic here
                return redirect('checkout')  # Redirect to the checkout page or another page
        else:
            address_form = AddressForm()

        cartItems = order.get_cart_items()
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'address_form': address_form, 'existing_address': existing_address}
        return render(request, 'store/checkout.html', context)
    else:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")


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
@transaction.atomic
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


@login_required
@transaction.atomic
def process_order(request):
    if not request.user.is_client:
        messages.info(request, "Vous n'êtes pas autorisé à accéder à cette page. Seuls les clients peuvent passer des commandes.")
        return redirect('home')

    transaction_id = datetime.datetime.now().timestamp()

    customer = request.user.customer

    # Récupérer toutes les commandes incomplètes pour le client
    incomplete_orders = Order.objects.select_for_update().filter(customer=customer, completed=False)

    if not incomplete_orders.exists():
        # Si aucune commande incomplète n'existe, renvoyer une erreur
        messages.error(request, "Aucune commande en cours n'a été trouvée.")
        return redirect('cart')  # Rediriger vers le panier

    for order in incomplete_orders:
        # Mettre à jour la commande avec la nouvelle transactionId et marquez-la comme complétée
        order.transactionId = transaction_id
        order.completed = True
        order.save()
        print(f"Order {order.id} updated with transaction ID {transaction_id} and marked as completed.")

        # Mettre à jour le statut de chaque OrderItem à 'En traitement'
        items = order.orderitem_set.all()
        for item in items:
            item.status = OrderItem.Status.PROCESSING
            item.ordered = True
            item.save()
            print(f"OrderItem {item.id} for order {order.id} updated to status 'Processing'.")

    messages.success(request, 'Votre commande a été passée avec succès. Merci!')
    return redirect('products')


@login_required()
def consultant_profile(request):
    consultant = request.user.consultant
    customers = Customer.objects.filter(consultant_applied=consultant)

    consultant_clients = []

    for customer in customers:
        ordered_items = OrderItem.objects.filter(customer=customer, ordered=True)
        not_ordered_items = OrderItem.objects.filter(customer=customer, ordered=False)
        consultant_clients.append((customer, ordered_items, not_ordered_items))

    return render(request, "store/consultant_profile.html", context={"consultant_clients": consultant_clients})
# Order to be updated by consultant
class OrderUpdateConsultantView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    form_class = OrderItemStatusForm
    template_name = "store/order_update_consultant.html"
    success_url = reverse_lazy('consultant-profile')
    context_object_name = 'my_order_item'

    # On utilise une transaction atomique pour garantir la cohérence des données
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True  # Afficher un message de mise à jour dans le template
        return context

        # Message de confirmation
        messages.success(self.request, "La commande a été mise à jour avec succès.")


class CategoryCRUDView(View):
    template_name = 'store/categories.html'
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        slug = request.GET.get('slug')

        if slug:
            category = Category.objects.get(slug=slug)
            form = self.form_class(instance=category)
        else:
            form = self.form_class()

        return render(request, self.template_name, {'form': form, 'categories': categories})

    def post(self, request, *args, **kwargs):
        slug = request.POST.get('slug')
        categories = Category.objects.all()

        if slug:
            category = Category.objects.get(slug=slug)
            form = self.form_class(request.POST, instance=category)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect('categorie')

        return render(request, self.template_name, {'form': form, 'categories': categories})

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = None
    fields = '__all__'
    def get_success_url(self):
        return reverse('categorie')
