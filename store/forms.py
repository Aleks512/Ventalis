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
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
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
        fields = ['status', 'comment']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'country', 'zipcode']

class OrderItemStatusForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status', 'comment']

    def __init__(self, *args, **kwargs):
        super(OrderItemStatusForm, self).__init__(*args, **kwargs)
        # Ajouter des attributs ou modifier les champs si nécessaire

        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 3})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

class CategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []

