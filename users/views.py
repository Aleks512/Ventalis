from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView
from .models import Consultant,NewUser, Customer
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
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

def consultant_signup(request):
    if request.method == 'POST':
        form = ConsultantCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = ConsultantCreationForm()
    return render(request, 'users/consultant_create.html', {'form': form})

class ConsultantListView(ListView):
    model = Consultant
    context_object_name = "consultants"

    def get_queryset(self):
        # Utilisez prefetch_related pour précharger les clients associés à chaque consultant
        return Consultant.objects.prefetch_related("clients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Consultants"
        return context

class CustomerListView(ListView):
    model = Customer
    context_object_name = "customers"
class NewUserListView(ListView):
    model = NewUser
    context_object_name = "users"

class WebAppLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with your desired URL after login
        return super().get(request, *args, **kwargs)


class CustomerHome(UserPassesTestMixin, DetailView):
    model = Customer
    template_name = "users/my_orders.html"
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.customer

    def get_object(self, queryset=None):
        id = self.request.user.customer.id
        return Customer.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()



