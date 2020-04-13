from django.db import models
from django.contrib.auth.models import User
from dynamic_models.models import AbstractModelSchema, AbstractFieldSchema
# Create your models here.

class DepartmentalHierarchy(models.Model):
	nodeId = models.CharField(max_length=150, primary_key=True)
	nodeName = models.CharField(max_length=150)
	isLeaf = models.BooleanField(default=False)

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
		if (UserRole.getObjectByUser(userId)):
			userRole = UserRole.getObjectByUser(userId)
			userRole.roleId = roleId
		else:
			userRole = cls(userId=userId, roleId=roleId)
		# do something with the book
		return userRole

	def getObjectByUser(user):
		try:
			userRole_obj = UserRole.objects.get(userId=user)
		except UserRole.DoesNotExist:
			userRole_obj = None
		return userRole_obj

	def __str__(self):
		return str(self.userId) + ' ------ ' + str(self.roleId)

class Base(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	nodeId = models.ForeignKey(DepartmentalHierarchy, on_delete=models.CASCADE)
	startFrom = models.DateField(null=True, blank=True)
	endTo = models.DateField(null=True, blank=True)

	@classmethod
	def create(cls, userId, nodeId):
		if (Base.getObjectByUser(userId)):
			base_obj = Base.getObjectByUser(userId)
			base_obj.nodeId = nodeId
		else:
			base_obj = cls(userId=userId, nodeId=nodeId)
		return base_obj

	def getObjectByUser(user):
		try:
			base_obj = Base.objects.get(userId=user)
		except Base.DoesNotExist:
			base_obj = None
		return base_obj

	def __str__(self):
		return str(self.userId) + ' ------ ' + str(self.nodeId)

class ModelSchema(AbstractModelSchema):
    pass

class FieldSchema(AbstractFieldSchema):
    pass