from django.urls import path

from . import views

app_name = 'forms'
urlpatterns = [
    path('', views.index, name='index'),
    path('createform', views.createform, name='createform'),
    path('parseFormTemplate', views.parseFormTemplate, name='parseFormTemplate')
]