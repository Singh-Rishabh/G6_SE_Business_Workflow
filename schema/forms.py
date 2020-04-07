from django import forms
from schema.models import DepartmentalHierarchy


def getAllNodeName():
	dept_all_object = DepartmentalHierarchy.objects.all()
	all_dept = set([x.nodeId for x in dept_all_object])
	choices = []
	for x in dept_all_object:
		if ((x.nodeId + '.1') not in all_dept):
			choices.append(tuple([x.nodeName, x.nodeName]))
	return choices

CHOICES = getAllNodeName()

class ProfileForm(forms.Form):
	first_name = forms.CharField(label='First name', max_length=30)
	last_name = forms.CharField(label='Last name', max_length=150)
	node_name = forms.CharField(label='What is your department Name',
				widget=forms.Select(choices=CHOICES))
	
	def clean_first_name(self):
		data = self.cleaned_data['first_name']
		return data

	def clean_last_name(self):
		data = self.cleaned_data['last_name']
		return data

	def clean_node_name(self):
		data = self.cleaned_data['node_name']
		return data