from django import forms

class SearchResult(forms.Form):
    your_search = forms.CharField(label='Enter App Name:', max_length=100)