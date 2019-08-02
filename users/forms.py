from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Grant
from dal import autocomplete


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

	def save(self, username, commit=True):
		instance = super(UserUpdateForm, self).save(commit=False)
		instance.username = username
		if commit:
			instance.save()
		return instance


class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['image', 'organization', 'position', 'degree', 'biography', 'link', 'ORCID']
		widgets = {
			'organization': autocomplete.ModelSelect2(url='organization-autocomplete')
		}

	def save(self, user, commit=True):
		instance = super(ProfileUpdateForm, self).save(commit=False)
		instance.user = user
		if commit:
			instance.save()
		return instance

class GrantForm(forms.ModelForm):

	class Meta:
		model = Grant
		fields = ['name', 'year_from', 'year_to', 'fund', 'amount', 'link']

	def save(self, profile, commit=True):
		instance = super(GrantForm, self).save(commit=False)
		instance.profile = profile
		if commit:
			instance.save()
		return instance
