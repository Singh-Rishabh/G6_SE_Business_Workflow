from django.urls import path
from . import views

app_name = 'schema'
urlpatterns = [
	path('', views.index, name='home'),
    path('upload_csv/dept/', views.upload_departmental_csv, name='upload_departmental_csv'),
    path('upload_csv/role/', views.upload_role_csv, name='upload_role_csv'),
    path('upload_csv/auth_info/', views.upload_auth_info_csv, name='upload_auth_info_csv'),
]

urlpatterns += [   
    path('profile/', views.update_profile, name='update_profile'),
]

