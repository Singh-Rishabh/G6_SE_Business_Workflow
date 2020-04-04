from django.db import models
from django.contrib.auth.models import User
from dynamic_models.models import AbstractModelSchema, AbstractFieldSchema
# Create your models here.

class DepartmentalHierarchy(models.Model):
	nodeId = models.CharField(max_length=150, primary_key=True)
	nodeName = models.CharField(max_length=150)

	def __str__(self):
		return self.nodeName


class RoleHierarchy(models.Model):
	roleId = models.CharField(max_length=150, primary_key=True)
	roleName = models.CharField(max_length=150)
	postFlag = models.BooleanField()

	def __str__(self):
		return self.roleName


class UserRole(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	roleId = models.ForeignKey(RoleHierarchy, on_delete=models.CASCADE)

	@classmethod
	def create(cls, userId, roleId):
		userRole = cls(userId=userId, roleId=roleId)
		# do something with the book
		return userRole

	def __str__(self):
		return str(self.userId + ' ------ ' + self.userRole)

class ModelSchema(AbstractModelSchema):
    pass

class FieldSchema(AbstractFieldSchema):
    pass