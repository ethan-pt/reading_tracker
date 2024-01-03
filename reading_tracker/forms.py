from django import forms
from .models import Book



class SearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        max_length=255,
        label='',
        strip=True,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'search-book-area',
            'name': 'text-area',
            'size': '50%',
            'placeholder': 'Enter title, author, publisher, or ISBN'
        })
    )


class CreateForm(forms.ModelForm):  
    class Meta:
        model = Book
        exclude = ['gbooks_id']