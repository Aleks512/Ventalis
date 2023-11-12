from django import forms

from users.models import Address
from .models import Category, Product, Order, OrderItem
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Product.objects.filter(name=name).exists():
            raise forms.ValidationError('Ce produit existe déjà.')
        return name


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Product.objects.filter(name=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Ce produit existe déjà.')
        return name

class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = []

# ------------ Orders --------------------
class OrderItemUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')

class OrderItemDeleteForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'country', 'zipcode']


# order_items=OrderItem.objects.all()
# for item in order_items:
#     order = item.order
#     prix = item.get_total
#     customer= item.customer
# orders = Order.objects.all()
# order_vide = Order.objects.filter(transactionId="")
# oroder1= Order.objects.get(id=7)


