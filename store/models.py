import random
import string
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save


class Category(models.Model):
    name = models.CharField(_("Nom"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), max_length=255, blank=True)

    class Meta:
        """Meta definition for Category."""
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

    def display_1000_units_price(self):
        return self.price * 1000

class Order(models.Model):
    customer = models.ForeignKey('users.Customer', verbose_name=_("Client"), on_delete=models.CASCADE)
    transactionId = models.CharField(max_length=20, blank=True, null=True)
    date_ordered = models.DateTimeField(_("Date de commande"), auto_now_add=True)
    completed = models.BooleanField(_("Commande complète"), default=False)
    comment = models.TextField(verbose_name=_("Commantaire sur commande"), blank=True, null=True)

    class Meta:
        ordering = ("-date_ordered",)
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
        # Check if the user has associated address.
        return not Address.objects.filter(user=self.customer).exists()

    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def get_transaction_id(self):  # Generate a random transaction ID
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', _('En attente')
        PROCESSING = 'PR', _('En traitement')
        SHIPPED = 'S', _('Expédié')
        DELIVERED = 'D', _('Livré')
        RETURNED = 'R', _('Retourné')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Statut de la commande"),
    )

    customer = models.ForeignKey('users.Customer', verbose_name=_("Client"), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_("Commande"), on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, verbose_name=_("Produit"), on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(_("Quantité"), default=1000)
    comment = models.TextField(verbose_name=_("Commantaire sur articles"), blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ("-date_added",)

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

    def get_absolute_url(self):
        return reverse('change_order_itemr', args=[str(self.id)])

class OrderItemStatusHistory(models.Model):
    order_item = models.ForeignKey('OrderItem', verbose_name=_("Article de commande"), on_delete=models.CASCADE)
    consultant = models.ForeignKey('users.Consultant', verbose_name=_("Consultant"), on_delete=models.CASCADE)
    customer = models.ForeignKey('users.Customer', verbose_name=_("Client"), on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=OrderItem.Status.choices,
        verbose_name=_("Nouveau statut de la commande"),
    )
    comment = models.TextField(verbose_name=_("Commentaire sur la modification"), blank=True, null=True)
    date_modified = models.DateTimeField(_("Date de modification"), auto_now_add=True)

    def __str__(self):
        return f"{self.order_item} - {self.status}"

    @receiver(pre_save, sender=OrderItem)
    def create_order_item_status_history(sender, instance, **kwargs):
        # Vérifier si l'objet OrderItem a déjà été enregistré en base de données (mise à jour plutôt que création)
        if instance.pk is not None:
            # Récupérer l'objet OrderItem enregistré en base de données pour comparer les changements
            old_order_item = OrderItem.objects.get(pk=instance.pk)
            # Récupérer le client associé à l'OrderItem
            customer = instance.customer

            # Récupérer le consultant associé au client
            consultant = customer.consultant_applied

            # Vérifier si le statut ou le commentaire a changé
            if instance.status != old_order_item.status or instance.comment != old_order_item.comment:
                # Enregistrer l'historique du statut
                OrderItemStatusHistory.objects.create(
                    order_item=instance,
                    consultant=consultant,
                    customer=customer,  # Utiliser le client associé à l'OrderItem
                    status=instance.status,
                    comment=instance.comment
                )