from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
class Category(models.Model):
    name = models.CharField(_("Nom"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)
    slug = models.SlugField(_("Slug"), unique=True, max_length=255)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Categories")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/{self.slug}/'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=_("Catégorie"), on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Prix"), max_digits=10, decimal_places=2)
    image = models.ImageField(_("Image"), upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    slug = models.SlugField(_("Slug"), unique=True, max_length=255)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url= ''
        return url


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug":self.slug})
    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey('users.Customer', verbose_name=_("Client"), on_delete=models.CASCADE)
    comment = models.TextField(verbose_name=_("Commantaire sur commande"),blank=True, null=True)
    date_ordered = models.DateTimeField(_("Date de commande"), auto_now_add=True)
    complete = models.BooleanField(_("Commande complète"), default=False)
    transaction_id = models.CharField(_("ID de transaction"), max_length=100, blank=True)

    def __str__(self):
        return str(self.id)
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.quantity >= 1000:
                shipping = True
        return shipping
    @property
    def get_cart_taotal(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    customer = models.ForeignKey('users.Customer', verbose_name=_("Client"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("Produit"), on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, verbose_name=_("Commande"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantité"), default=1000)
    comment = models.TextField(verbose_name=_("Commantaire sur articles"), blank=True, null=True)
    date_added = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Client"), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_("Commande"), on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(_("Adresse"))
    city = models.CharField(_("Ville"), max_length=100)
    country = models.CharField(_("Pays"), max_length=100)
    zipcode = models.CharField(_("Code postal"), max_length=20)
    date_added = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'Addresses'
