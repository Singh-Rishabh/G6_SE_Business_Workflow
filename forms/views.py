from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

form_field_types = {

	'textarea' : 'textarea',
	'number' : 'number',
	'date' : 'date',
	'radio' : 'radio',
	'checkbox' : 'checkbox'

}

def index(request):
    return HttpResponse("Hello, world. You're at the forms index.")

def home(request):
	return render(request , 'forms/index.html')

def createform(request):
	return render(request , 'forms/createform.html', {'form_field_types' : form_field_types})
