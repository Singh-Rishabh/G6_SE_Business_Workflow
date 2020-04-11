from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import FormTemplate, FieldDescription
from django.urls import reverse
from django.core.files import File
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
		
def validate_title(request):

	newTitle=request.GET.get('formTitle',None)
	data = {
		'is_taken': FormTemplate.objects.filter(formTitle__exact=newTitle).exists()
	}
	if data['is_taken']:
		data['error_message'] = 'A form with this title already exists.'
	return JsonResponse(data)
	
def store_html(request):

	newTitle=request.GET.get('formTitle',None)
	data = {
		'is_taken': FormTemplate.objects.filter(formTitle__exact=newTitle).exists()
	}
	data['error_message'] = 'Hi There'
	return JsonResponse(data)
	# title = request.GET.get('formTitle' , None)
	# html = request.GET.get('formHtml' , None)	
	# with open('./uploads/'+title+'.html', 'w') as f:
	# 	myfile = File(f)
	# 	myfile.write(html)
	# myfile.close()
	# formTemplate = FormTemplate(formTitle=request.POST['formTitle'], formDescription=request.POST['formDescriptor'], formHtml=myfile)