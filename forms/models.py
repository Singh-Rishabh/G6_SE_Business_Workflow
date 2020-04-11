from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db import models 
from django.db.models import Model 

# Create your models here.
## This Table will basically store form name, description and date of Creation
class FormTemplate(models.Model) :

    formTitle = models.CharField(max_length=200)
    formDescription = models.TextField()
    dateOfCreation = models.DateTimeField(auto_now=True)
    # formHtml = models.FileField(upload_to='uploads/', null = True)

## This will stroe all fields related to form Question field name, field type and labels
class FieldDescription(models.Model) :

    template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    questionTag = models.CharField(max_length=50)
    typeOfField = models.CharField(max_length=20)
    labelField = ArrayField(models.CharField(max_length=50, blank=True), null=True, default=None)
