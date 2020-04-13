import csv, io
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User
from schema.models import DepartmentalHierarchy, RoleHierarchy, UserRole, Base
from django.contrib.auth.decorators import login_required
from schema.forms import ProfileForm

@login_required
def index(request):
	context = {}
	if (request.user.is_authenticated):
		user = request.user
		context['username'] = user.username
		context['password'] = user.password
		base_obj = Base.getObjectByUser(user)
	else :
		return HttpResponseRedirect(reverse("login"))

	if (base_obj):
		template = "schema/index.html"
		return render(request, template, context)
	else:
		if (not(request.user.is_superuser)):
			return HttpResponseRedirect(reverse("schema:update_profile"))
		else:
			template = "schema/index.html"
			return render(request, template, context)
	

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
			        defaults={
				    'nodeName':column[1]}
			    )
			_, created = DepartmentalHierarchy.objects.update_or_create(
			        nodeId='None',
			        defaults={
				    'nodeName':'No-Department'}
			    )
			dept_all_object = DepartmentalHierarchy.objects.all()
			all_dept = set([x.nodeId for x in dept_all_object])
			choices = []
			for x in dept_all_object:
				if ((x.nodeId + '.1') not in all_dept):
					x.isLeaf = True
				else:
					x.isLeaf = False
				x.save()
			context = {}

		except Exception as e:
			return render(request, template, {'error_message': "Unable to upload file. "+repr(e)})

		return HttpResponseRedirect(reverse("schema:home"))
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
			        defaults={
				    'roleName':row[1],
				    'postFlag':row[2]}
			    )
			context = {}

		except Exception as e:
			return render(request, template, {'error_message': "Unable to upload file. "+repr(e)})
		
		return HttpResponseRedirect(reverse("schema:home"))
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
				user, created = User.objects.update_or_create(username=column[0].split('@')[0],
															defaults={'email':column[0]})
				user.set_password(column[1])
				roleObj = get_object_or_404(RoleHierarchy, roleName=column[2])
				userRole = UserRole.create(user, roleObj)
				user.save()
				userRole.save()
			context = {}

		except Exception as e:
			return render(request, template, {'error_message': "Unable to upload file. "+repr(e)})

		return HttpResponseRedirect(reverse("schema:home"))
	else:
		return HttpResponseForbidden('You cannot upload or change Authentication Information')


'''
	TODO - backend handling of None Department .... 
'''
@login_required
def update_profile(request):
	if request.user.is_authenticated:
		user = request.user
		if request.method == 'POST':
			# Create a form instance and populate it with data from the request (binding):
			form = ProfileForm(request.POST)
			if form.is_valid():
				user.first_name = form.cleaned_data['first_name']
				user.last_name = form.cleaned_data['last_name']
				node_name = form.cleaned_data['node_name']
				if (node_name != 'None'):
					dept_hirerachy_obj = get_object_or_404(DepartmentalHierarchy, nodeName=node_name)
					base_obj = Base.create(user, dept_hirerachy_obj)
					user.save()
					base_obj.save()
				else :
					user.save()
				return HttpResponseRedirect(reverse("schema:home"))				

		# If this is a GET (or any other method) create the default form
		else:
			base_obj = Base.getObjectByUser(user)
			form = ProfileForm()

		context = {
			'form': form,
			'user': user,
			'base':base_obj
		}

		return render(request, 'schema/update_profile.html', context)

	else:
		return HttpResponseRedirect(reverse("login"))
