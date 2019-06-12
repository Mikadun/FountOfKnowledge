from django import forms

class FilterForm(forms.Form):
	author = forms.CharField(label='Author name:', max_length=100, required=False)