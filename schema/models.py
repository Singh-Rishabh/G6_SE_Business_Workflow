from django.db import models

# Create your models here.

class DepartmentalHierarchy(models.Model):
	nodeId = models.CharField(max_length=150,unique=True)
	nodeName = models.CharField(max_length=150)

	def __str__(self):
		return self.nodeName


class RoleHierarchy(models.Model):
	roleId = models.CharField(max_length=150,unique=True)
	roleName = models.CharField(max_length=150)
	postFlag = models.BooleanField()

	def __str__(self):
		return self.roleName