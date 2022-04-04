from django.contrib.auth.models import User
from django import forms
class MainForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password']
class GymMainForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password']

