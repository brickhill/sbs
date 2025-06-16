from django import forms


class SearchSite(forms.Form):
    query = forms.CharField(label="Search",
     help_text="Search the site")

class LoginPage(forms.Form):
    username= forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", max_length=20,
                               widget=forms.PasswordInput())

