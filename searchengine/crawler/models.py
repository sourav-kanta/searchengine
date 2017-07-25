# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms 
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db import models

# Create your models here.

class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='Email')
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput())
	password2 = forms.CharField(label='Retype',widget=forms.PasswordInput())

	def clean_username(self):
		print "Called clean username"
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		except MultipleObjectsReturned:
			raise forms.ValidationError('Username is already taken.')
		raise forms.ValidationError('Username is already taken.')

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
		if password1 == password2:
			return password2
		raise forms.ValidationError('Passwords do not match.')

