from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """Creates Product form"""
    class Meta:
        model = Product
        fields = '__all__'       

    
    def __init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.object.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-dark rounded-1'
