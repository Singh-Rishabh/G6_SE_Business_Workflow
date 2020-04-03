from django.contrib import admin

# Register your models here.
from .models import DepartmentalHierarchy, RoleHierarchy, UserRole

class DeptHierarchyAdmin(admin.ModelAdmin):
	list_display = ('nodeId', 'nodeName')

@admin.register(RoleHierarchy)
class RoleHierarchyAdmin(admin.ModelAdmin):
	list_display = ('roleId', 'roleName', 'postFlag')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
	list_display = ( 'userId', 'roleId')

admin.site.register(DepartmentalHierarchy, DeptHierarchyAdmin)