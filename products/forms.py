from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """Creates Product form"""
    class Meta:
        model = Product

        fields = ('category', 'name', 'price', 'description',
                  'image', 'sku',)
        widgets = {
                    'category': forms.Select(
                        attrs={'class': 'form-select'}),                    
                    }     

    
    def __init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.object.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-1'
