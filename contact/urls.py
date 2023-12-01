# urls.py
from django.urls import path
from .views import contact

urlpatterns = [
    # Other paths...
    path('contact/', contact, name='contact'),
]