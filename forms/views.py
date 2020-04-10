from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import FormTemplate, FieldDescription
from django.urls import reverse
# Create your views here.

form_field_types = {

	'textarea' : 'textarea',
	'number' : 'number',
	'date' : 'date',
	'radio' : 'radio',
	'checkbox' : 'checkbox'

}

def index(request):

	recent_forms = FormTemplate.objects.all()	
	return render(request , 'forms/index.html', {'recent_forms' : recent_forms})

def home(request):
	return render(request , 'forms/index.html')

def createform(request):
	return render(request , 'forms/createform.html', {'form_field_types' : form_field_types})

def parseFormTemplate(request) :

	try :
		# Get the query dict in name value pair
		formTemplate = FormTemplate(formTitle=request.POST['formTitle'], formDescription=request.POST['formDescriptor'])
		formTemplate.save()
		
		labelsIndex = list()
		questionList = request.POST.getlist('Question[]')
		answerList = request.POST.getlist('Answer[]')

		for index, ans in enumerate(answerList) :
			if len(ans) > 0 :
				if ans[-1] == "#" :
					labelsIndex.append(index)
		
		for counter, question in enumerate(questionList) :
			typeOfField = answerList[labelsIndex[counter]][:-1]
			if counter == len(labelsIndex) - 1 :
				labelsList = answerList[labelsIndex[counter]+1 : ]
			else :
				labelsList = answerList[labelsIndex[counter]+1 : labelsIndex[counter+1]]

			formTemplate.fielddescription_set.create(questionTag=question, typeOfField=typeOfField, labelField=labelsList)

	except KeyError :
		return render(request, 'forms/index.html')
	else :
		return HttpResponseRedirect(reverse('forms:index'))
		