from django import forms



class SearchForm(forms.Form):
    search_query = forms.CharField(
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


class CreateForm(forms.Form):
    BOOK_TYPE_CHOICES = [
        ('paper-book', 'paper book'),
        ('e-book', 'e-book'),
        ('audio-book', 'audio book')
    ]

    title = forms.CharField(max_length=255)
    author = forms.CharField(max_length=255)
    publisher = forms.CharField(max_length=255)
    gbooks_id = forms.CharField(max_length=12)
    book_type = forms.ChoiceField(choices=BOOK_TYPE_CHOICES)
    length_pages = forms.IntegerField()
    length_time = forms.DurationField()