from django import forms

class AddPointForm(forms.Form):
	maplerId = forms.IntegerField(widget=forms.HiddenInput())
	description = forms.CharField(max_length=200)
	longitude = forms.FloatField()
	latitude = forms.FloatField()