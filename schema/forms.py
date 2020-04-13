from django import forms
from . import models

class ProfileForm(forms.Form):
	first_name = forms.CharField(label='First name', max_length=30)
	last_name = forms.CharField(label='Last name', max_length=150)
	node_name = forms.ModelChoiceField(queryset=
				models.DepartmentalHierarchy.objects.filter(isLeaf=True))
	
	def clean_first_name(self):
		data = self.cleaned_data['first_name']
		return data

	def clean_last_name(self):
		data = self.cleaned_data['last_name']
		return data

	def clean_node_name(self):
		data = self.cleaned_data['node_name']
		return data