from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Creates Post form"""

    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'content',
                  'tag', 'featured_image', 'status',)

        widgets = {
                    'tag': forms.Select(
                        attrs={'class': 'form-select'}),
                    'status': forms.Select(attrs={'class': 'form-select'}),
                    }
