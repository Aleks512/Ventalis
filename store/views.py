from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductCreateForm, ProductUpdateForm, ProductDeleteForm
from .models import Category, Product


def store(request):

	return render(request, 'store/store.html')

def cart(request):

	return render(request, 'store/cart.html')

def checkout(request):

	return render(request, 'store/checkout.html')

def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')  # Récupérer la catégorie sélectionnée
    return render(request, "store/products.html", context={"products": products, "categories": categories, "selected_category": selected_category})

@login_required()
def products_list_mng(request):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "store/products_list_mng.html", context={"products":products, "categories": categories})
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, "store/product_detail.html", context={"product":product})

@login_required()
def product_create_view(request):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    form = ProductCreateForm(request.POST or None, request.FILES or None)
    categories = Category.objects.all()
    if form.is_valid():
        form.save()
        return redirect('products-list-mng')
    return render(request, 'store/product_create.html', {'form': form,"categories": categories})

@login_required()
def product_update_view(request, slug):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    product = get_object_or_404(Product, slug=slug)
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products-list-mng')
    return render(request, 'store/product_update.html', {'form': form, 'product': product})

@login_required()
def product_delete_view(request, slug):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    product = get_object_or_404(Product, slug=slug)
    form = ProductDeleteForm(request.POST or None, instance=product)
    if request.method == 'POST':
        product.delete()
        return redirect('products-list-mng')
    return render(request, 'store/product_delete.html', {'form': form, 'product': product})
