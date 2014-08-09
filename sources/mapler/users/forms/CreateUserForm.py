from django import forms

class CreateUserForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    mail = forms.EmailField(required=False)
    agreement = forms.BooleanField(required = True)