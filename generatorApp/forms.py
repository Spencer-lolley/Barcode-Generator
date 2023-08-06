from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    copies = forms.IntegerField(min_value=1, initial=1)  # Add an IntegerField for the number of copies

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'school', 'copies']  # Include the 'copies' field
