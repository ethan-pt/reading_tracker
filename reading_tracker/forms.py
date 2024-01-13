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
        fields = '__all__'
        labels = {
            'book_type': 'What kind of book is it?',
            'length_pages': 'How many pages does it have?',
            'length_time': 'How long is it?'
        }
        widgets = {
            'length_time': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        }