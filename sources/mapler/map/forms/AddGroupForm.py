from django import forms

class AddGroupForm(forms.Form):
	maplerId = forms.IntegerField(widget=forms.HiddenInput())
	name = forms.CharField(max_length=20)
	description = forms.CharField(max_length=200)
