import csv, io
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User
from schema.models import DepartmentalHierarchy, RoleHierarchy, UserRole
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	if request.user.is_superuser:
		template = "schema/index.html"
		return render(request, template, {})
	else:
		return HttpResponseForbidden('You cannot upload or change schema!')

# Create your views here.
# one parameter named request
@login_required
def upload_departmental_csv(request):
	template = "schema/upload_departmental_csv.html"
	data = {}
	if request.user.is_superuser:
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
	else:
		return HttpResponseForbidden('You cannot upload or change Departmental Hierarchy')


@login_required
def upload_role_csv(request):
	template = "schema/upload_role_csv.html"
	data = {}
	if request.user.is_superuser:
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
	else:
		return HttpResponseForbidden('You cannot upload or change Role Hierarchy')

@login_required
def upload_auth_info_csv(request):
	template = "schema/upload_auth_info_csv.html"
	data = {}
	if request.user.is_superuser:
		if request.method == "GET":
			return render(request, template, data)
	    # if not GET, then proceed
		try:
			csv_file = request.FILES["auth_info_csv_file"]
			if not csv_file.name.endswith('.csv'):
				return render(request, template, {'error_message': "File is not of CSV type"})
	        
			data_set = csv_file.read().decode('UTF-8')
			# setup a stream which is when we loop through each line we are able to handle a data in a stream
			io_string = io.StringIO(data_set)
			for column in csv.reader(io_string, delimiter=',', quotechar="|"):
			    user = User.objects.create_user(username=column[0], 
			    								email=column[1], 
			    								password=column[2])

			    roleId = get_object_or_404(RoleHierarchy, roleId=column[3])
			    userRole = UserRole.create(user, roleId)
			    user.save()
			    userRole.save()
			    # user.authentication.roleId = get_object_or_404(RoleHierarchy, roleId=column[3])
			    # _, created = Authentication.objects.update_or_create(
			    #     user=user,
				   #  roleId=get_object_or_404(RoleHierarchy, roleId=column[3])
			    # )
			context = {}

		except Exception as e:
			return render(request, template, {'error_message': "Unable to upload file. "+repr(e)})

		return HttpResponseRedirect(reverse("schema:index"))
	else:
		return HttpResponseForbidden('You cannot upload or change Authentication Information')