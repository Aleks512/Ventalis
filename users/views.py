from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from store.models import OrderItem
from .models import Consultant,NewUser, Customer
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConsultantCreationForm, CustomerCreationForm

def home(request):
    return render(request, 'home.html')

def presentation(request):

    return render(request, "presentation.html")

def signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomerCreationForm()
    return render(request, 'users/signup.html', {'form': form})
#
# def consultant_signup(request):
#     if request.method == 'POST':
#         form = ConsultantCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=password)
#             login(request, user)
#             return redirect('consultant-profile')
#     else:
#         form = ConsultantCreationForm()
#     return render(request, 'users/consultant_list.html', {'form': form})

# FIXME: Ajouter l'authentification pour l" dministrateur
class CustomerListView(ListView):
    model = Customer
    context_object_name = "customers"

# FIXME: Ajouter l'authentification pour l" dministrateur
def customers_relations(request):
    employees = Consultant.objects.all().order_by('-date_joined')
    consultant_clients = []  # Create a list to store clients for each consultant

    for employee in employees:
        clients = Customer.objects.filter(consultant_applied=employee)
        consultant_clients.append((employee, clients))  # Append a tuple of (consultant, clients) to the list

    customers = Customer.objects.all()
    return render(request, 'users/customer_list.html', context={'consultant_clients': consultant_clients, 'customers': customers})

# FIXME: Ajouter l'authentification pour l" dministrateur
class NewUserListView(ListView):
    model = NewUser
    context_object_name = "users"

class WebAppLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


@login_required
def customer_profile(request):
    # Assuming the user is authenticated, retrieve their customer profile
    ordered_items = OrderItem.objects.filter(customer=request.user, ordered=True).order_by("status", "-date_added")
    not_ordered_items = OrderItem.objects.filter(customer=request.user, ordered=False).order_by("status", "-date_added")

    context = {
        "ordered_items": ordered_items,
        "not_ordered_items": not_ordered_items,
    }

    return render(request, "users/customer_profile.html", context)

# class CustomerHome(UserPassesTestMixin, DetailView):
#     model = Customer
#     template_name = "users/my_orders.html"
#     fields = '__all__'
#
#     def test_func(self):
#         return self.request.user.is_authenticated and self.request.user.customer
#
#     def get_object(self, queryset=None):
#         id = self.request.user.customer.id
#         return Customer.objects.get(id=id)

    #
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     customer = self.get_object()


# class ConsultantListView(ListView):
#     model = Consultant
#     context_object_name = "consultants"
#
#     def get_queryset(self):
#         return Consultant.objects.prefetch_related("clients")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Consultants"
#         return context
#
# class ConsultantCreateView(CreateView):
#     model = Consultant
#     form_class = ConsultantCreationForm
#     template_name = 'users/consultant_list.html'
#     success_url = '/consultants/'
#     context_object_name = "consultants"
#
#
#
# class ConsultantUpdateView(UpdateView):
#     model = Consultant
#     form_class = ConsultantCreationForm
#     template_name = 'users/consultant_list.html'
#     success_url = '/consultants/'
#     context_object_name = "consultants"
#
#     # get context data needed as objects in CBV is not iterable
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Consultants"
#         context['consultants'] = [self.object]  # Utilisez une liste pour rendre l'objet itérable
#         return context

# FIXME: Ajouter l'authentification pour l" dministrateur
# FIXME: Ajouter success message ou error message
class ConsultantCreateView(View):
    template_name = 'users/consultant_list.html'
    form_class = ConsultantCreationForm

    def get(self, request, *args, **kwargs):
        """
        GET method for ConsultantCreateView to render the form and list of consultants
        """
        consultants = Consultant.objects.all() # Get all consultants
        consultant_id = request.GET.get('pk') # Get the consultant ID from the query string
        form = self.form_class()    # Create a new form instance

        if consultant_id:  # If the consultant ID is present in the query string
            consultant = get_object_or_404(Consultant,pk=consultant_id) # Get the consultant object
            form = self.form_class(instance=consultant) # Create a form instance with the consultant object

        return render(request, self.template_name, {'form': form, 'consultants': consultants})

    def post(self, request, *args, **kwargs): # POST method for ConsultantCreateView to save the form data
        consultant_id = request.GET.get('pk') # Get the consultant ID from the query string
        consultants = Consultant.objects.all() # Get all consultants
        form = self.form_class(request.POST) # Create a form instance with the POST data

        if consultant_id: # If the consultant ID is present in the query string
            category = get_object_or_404(Consultant, pk=consultant_id) # Get the consultant object
            form = self.form_class(request.POST, instance=category) # Create a form instance with the consultant object

        if form.is_valid(): # If the form is valid
            form.save() # Save the form data
            return redirect('consultants') # Redirect to the consultants list view

        return render(request, self.template_name, {'form': form, 'consultants': consultants})

class ConsultantDeleteView(DeleteView):
    model = Consultant
    template_name = 'users/consultant_list.html'
    success_url = '/consultants/'
    context_object_name = "consultants"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Consultants"
        context['consultants'] = [self.object]  # Utiliser une liste pour rendre l'objet itérable
        return context





