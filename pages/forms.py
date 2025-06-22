from django import forms


class SearchSite(forms.Form):
    query = forms.CharField(
                            label="Enter search string",
                            widget=forms.TextInput(
                                                   attrs={'class': 'form-control'}
                                                   )
                            )


class LoginPage(forms.Form):
    username = forms.CharField(label="Username", max_length=20,
                               widget=forms.TextInput(
                                attrs={'class': 'form-control'}
                                                ))
    password = forms.CharField(label="Password", max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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
    message = forms.CharField(label="Your message", max_length=2000,
                             widget=forms.Textarea(attrs={'class': 'form-control'})
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
