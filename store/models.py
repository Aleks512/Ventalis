import random
import string
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings



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
    discount_price = models.DecimalField(_("Prix"), max_digits=10, decimal_places=2, blank=True, null=True)
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
    transactionId = models.CharField(max_length=20, blank=True, null=True)
    date_ordered = models.DateTimeField(_("Date de commande"), auto_now_add=True)
    completed = models.BooleanField(_("Commande complète"), default=False)
    comment = models.TextField(verbose_name=_("Commantaire sur commande"), blank=True, null=True)
    def __str__(self):
        return str(self.id)
    def has_high_quantity_items(self):
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.quantity >= 1000:
                return True
        return False

    @property
    def need_shipping_address(self):
        from users.models import Address # # Import Address locally, not at the beginning of the file, if not circular import issue
        # Check if the user has an associated address.
        return not Address.objects.filter(user=self.customer).exists()



    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def get_transaction_id(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    def save(self, *args, **kwargs):
        if not self.transactionId:
            self.transactionId= self.get_transaction_id()
        super().save(*args, **kwargs)
class OrderItem(models.Model):
    customer = models.ForeignKey('users.Customer', verbose_name=_("Client"), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_("Commande"), on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, verbose_name=_("Produit"), on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(_("Quantité"), default=1000)
    comment = models.TextField(verbose_name=_("Commantaire sur articles"), blank=True, null=True)
    date_added = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    @property
    def get_total_discount_price(self):
        total = self.product.discount_price * self.quantity
        return total


