from django import forms

class SearchResult(forms.Form):
    your_search = forms.CharField(label='Enter App Name:', max_length=100)

class SubmitResult(forms.Form):
    submit_url = forms.CharField(label='Submit URL', max_length=200)