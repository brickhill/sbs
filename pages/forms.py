from django import forms


class SearchSite(forms.Form):
    query = forms.CharField(
                            label="Search",
                            help_text="Search the site"
                            )


class LoginPage(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", max_length=20,
                               widget=forms.PasswordInput())


class ContactForm(forms.Form):

    name = forms.CharField(label="name",
                           max_length=20,
                           widget=forms.TextInput(
                                attrs={'class': 'form-control'}
                                                )
                           )
    email = forms.CharField(label="email",
                            max_length=50,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}
                                                   )
                            )

    class Meta:

        widgets = {
            'name': forms.TextInput(
                attrs={
                        # 'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
