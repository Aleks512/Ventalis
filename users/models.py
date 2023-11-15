import random
import string
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from Ventalis import settings
from store.models import Order


class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def _create_user(self, email, password = None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("first_name", "Administrateur")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('company', 'Ventalis')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'),unique=True, blank=False, max_length=255)
    first_name = models.CharField(_("Prénom"), max_length=100)
    last_name = models.CharField(_("Nom de famille"), max_length=50)
    company = models.CharField(_("Société"), max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email


class Consultant(NewUser):
    MATRICULE_LENGTH = 5
    matricule = models.CharField(_("Matricule"),max_length=MATRICULE_LENGTH, unique=True)


    def generate_random_matricule(self):
        while True:
            matricule = ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.MATRICULE_LENGTH))
            if not Consultant.objects.filter(matricule=matricule).exists():
                return matricule

    def generate_email(self):
        base_email = f'{self.first_name.lower()}.{self.last_name.lower()}'
        email = f'{base_email}@ventalis.com'
        count = 1
        while NewUser.objects.filter(email=email).exists():
            email = f'{base_email}.{count}@ventalis.com'
            count += 1
        return email

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule= self.generate_random_matricule()
        if not self.email:
            self.email= self.generate_email()
        if not self.is_staff:
            self.is_staff = True
        if not self.is_employee:
            self.is_employee = True
        if not self.company:
            self.company = 'Ventalis'
        super().save(*args, **kwargs)

    class Meta:
        db_table = "consultants"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_clients_count(self):
        return self.clients.count()

    def get_absolute_url(self):
        return reverse('consultant-home', kwargs={'matricule': self.matricule})

class Customer(NewUser):
    consultant_applied = models.ForeignKey('Consultant', on_delete=models.CASCADE, null=True, related_name='clients')

    class Meta:
        db_table = "customers"

    def assign_consultant_to_client(self):
        if not self.consultant_applied:
            consultant = Consultant.objects.annotate(num_clients=models.Count('clients')).order_by('num_clients').first()
            self.consultant_applied = consultant
            self.save()
            return consultant

    def save(self, *args, **kwargs):
        if not self.is_client:
            self.is_client = True
        if not self.consultant_applied:
            self.consultant_applied = self.assign_consultant_to_client()
        super().save(*args, **kwargs)

class Address(models.Model):
    user = models.ForeignKey(Customer, verbose_name=_("Client"), on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, verbose_name=_("Commande"), on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(_("Street"), max_length=100)
    city = models.CharField(_("Ville"), max_length=100)
    country = models.CharField(_("Pays"), max_length=100)
    zipcode = models.CharField(_("Code postal"), max_length=20)
    date_added = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country} {self.zipcode}"

    class Meta:
        verbose_name_plural = 'Addresses'
    def get_edit_url(self):
        return reverse('edit_address', args=[str(self.id)])