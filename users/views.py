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
    user_agent = request.META.get('HTTP_USER_AGENT')
    print('user agent: ',user_agent)
    ip_address = request.META.get('REMOTE_ADDR')
    print('IP adresse',ip_address)
    my_cookie_csrf = request.COOKIES.get('csrftoken')
    print("MY CSRF COOKIE : ",my_cookie_csrf)
    my_cookie_sessionid = request.COOKIES.get('sessionid')
    print("MY SESSION ID COOKIE : ", my_cookie_sessionid)
    content_type=request.META['CONTENT_TYPE']
    print("cintent-tyoe", content_type)
    user = request.user
    if user.is_authenticated:
        print(user.__dict__)
    else:
        print("No user is currently logged in.")
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


class CustomerListView(ListView):
    model = Customer
    context_object_name = "customers"


def customers_relations(request):
    employees = Consultant.objects.all().order_by('-date_joined')
    consultant_clients = []  # Create a list to store clients for each consultant

    for employee in employees:
        clients = Customer.objects.filter(consultant_applied=employee)
        consultant_clients.append((employee, clients))  # Append a tuple of (consultant, clients) to the list

    customers = Customer.objects.all()
    return render(request, 'users/customer_list.html', context={'consultant_clients': consultant_clients, 'customers': customers})

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
    ordered_items = OrderItem.objects.filter(customer=request.user.customer, ordered=True).order_by("status")
    not_ordered_items = OrderItem.objects.filter(customer=request.user.customer, ordered=False).order_by("status")

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


class ConsultantCreateView(View):
    template_name = 'users/consultant_list.html'
    form_class = ConsultantCreationForm

    def get(self, request, *args, **kwargs):
        consultants = Consultant.objects.all()
        consultant_id = request.GET.get('pk')
        form = self.form_class()

        if consultant_id:
            consultant = get_object_or_404(Consultant,pk=consultant_id)
            form = self.form_class(instance=consultant)

        return render(request, self.template_name, {'form': form, 'consultants': consultants})

    def post(self, request, *args, **kwargs):
        consultant_id = request.GET.get('pk')
        consultants = Consultant.objects.all()
        form = self.form_class(request.POST)

        if consultant_id:
            category = get_object_or_404(Consultant, pk=consultant_id)
            form = self.form_class(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect('consultants')

        return render(request, self.template_name, {'form': form, 'consultants': consultants})

class ConsultantDeleteView(DeleteView):
    model = Consultant
    template_name = 'users/consultant_list.html'
    success_url = '/consultants/'
    context_object_name = "consultants"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Consultants"
        context['consultants'] = [self.object]  # Utilisez une liste pour rendre l'objet itérable
        return context





