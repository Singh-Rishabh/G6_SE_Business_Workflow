from django.db import models
from django.contrib.auth.models import User
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