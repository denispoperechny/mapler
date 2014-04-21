from django import forms

class CreateUserForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField()
    mail = forms.EmailField(required=False)