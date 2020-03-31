import csv, io
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from schema.models import DepartmentalHierarchy, RoleHierarchy


def index(request):
	return HttpResponse("You have uploaded file successfully.")

# Create your views here.
# one parameter named request
def upload_departmental_csv(request):
	template = "schema/upload_departmental_csv.html"
	data = {}
	if request.method == "GET":
		return render(request, template, data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["departmental_csv_file"]
		if not csv_file.name.endswith('.csv'):
			return render(request, template, {'error_message': "File is not of CSV type"})
        
		data_set = csv_file.read().decode('UTF-8')
		# setup a stream which is when we loop through each line we are able to handle a data in a stream
		io_string = io.StringIO(data_set)
		for column in csv.reader(io_string, delimiter=',', quotechar="|"):
		    _, created = DepartmentalHierarchy.objects.update_or_create(
		        nodeId=column[0],
			    nodeName=column[1]
		    )
		context = {}

	except Exception as e:
		return render(request, template, {'error_message': "Unable to upload file. "+repr(e)})

	return HttpResponseRedirect(reverse("schema:index"))



def upload_role_csv(request):
	template = "schema/upload_role_csv.html"
	data = {}
	if request.method == "GET":
		return render(request, template, data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["role_csv_file"]
		if not csv_file.name.endswith('.csv'):
			return render(request, template, {'error_message': "File is not of CSV type"})
		
		data_set = csv_file.read().decode('UTF-8')
		# setup a stream which is when we loop through each line we are able to handle a data in a stream
		io_string = io.StringIO(data_set)
		for row in csv.reader(io_string, delimiter=',', quotechar="|"):
		    _, created = RoleHierarchy.objects.update_or_create(
		        roleId=row[0],
			    roleName=row[1],
			    postFlag=row[2]
		    )
		context = {}

	except Exception as e:
		return render(request, template, {'error_message': "Unable to upload file. "+repr(e)})
	
	return HttpResponseRedirect(reverse("schema:index"))
