from django import forms

class SearchResult(forms.Form):
    your_search = forms.CharField(label='Search By Name', max_length=100)

class SubmitResult(forms.Form):
    submit_url = forms.CharField(label='Submit URL', max_length=200)

class CountriesList(forms.Form):
    countries_list = forms.CharField(label='Country List', max_length=200)

