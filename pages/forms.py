from django import forms


class SearchSite(forms.Form):
    query = forms.CharField(label="Search",
     help_text="Search the site")