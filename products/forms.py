from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Review

class ProductForm(forms.ModelForm):
    """Creates Product form"""
    class Meta:
        model = Product

        fields = ('category','sku', 'name', 'price', 'description',
                  'image', 'on_sale', 'sale_price',)
        widgets = {
                    'category': forms.Select(
                        attrs={'class': 'form-select'}),
                    'price': forms.NumberInput(
                        attrs={'min': '0', 'max': '5000'}),
                    'sale_price': forms.NumberInput(
                        attrs={'min': '0', 'max': '5000'}),
                    }     

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput,
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        category_view_name = [(c.id, c.get_view_name()) for c in categories]

        self.fields['category'].choices = category_view_name
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-1'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)
