from django.shortcuts import get_object_or_404,render
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

	recent_forms = FormTemplate.objects.all()	
	return render(request , 'forms/index.html', {'recent_forms' : recent_forms})

def createform(request) :
	return render(request , 'forms/createform.html', {'form_field_types' : form_field_types})

def renderTemplate(request, form_id) :

	form = get_object_or_404(FormTemplate, pk=form_id)
	return render(request, 'forms/renderTemplate.html', {'form' : form, 'fieldList' : form.fielddescription_set.all()})

def parseFormTemplate(request) :

	try :
		# Get the query dict in name value pair
		formTemplate = FormTemplate.objects.get(formTitle=request.POST['formTitle'])
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
		#return {'redirect' : 'forms/index.html'}
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
	try:
		title=request.GET.get('formTitle',None)
		html = request.GET.get('formHtml' , None)
		descriptor = request.GET.get('formDescriptor' , None)
		formTemplate = FormTemplate(formTitle=title, formDescription=descriptor , formHtml=html)
		formTemplate.save()
	except KeyError:
		data = {
			'error_message': 'Error'
		}
	else:
		data = {
			'error_message': 'Successfull'
		}
	return JsonResponse(data)