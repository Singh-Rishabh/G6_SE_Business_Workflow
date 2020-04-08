from django.db.models.signals import post_save
from django.dispatch import receiver
from schema.models import RoleHierarchy, ModelSchema, FieldSchema, Base, UserRole


@receiver(post_save, sender=RoleHierarchy)
def create_role_tables(sender, instance, created, **kwargs):
	if instance.postFlag=='True':
		table_exists = ModelSchema.objects.filter(name=instance.roleName).exists()
		table_does_not_exist = not table_exists
		if created or table_does_not_exist:
			role_model_schema = ModelSchema.objects.create(name=instance.roleName)

			if FieldSchema.objects.filter(name='userId').exists():
				user_id_field_schema = FieldSchema.objects.get(name='userId')
			else:
				user_id_field_schema = FieldSchema.objects.create(name='userId', data_type='character')

			if FieldSchema.objects.filter(name='nodeId').exists():
				node_id_field_schema = FieldSchema.objects.get(name='nodeId')
			else:
				node_id_field_schema = FieldSchema.objects.create(name='nodeId', data_type='character')

			if FieldSchema.objects.filter(name='startFrom').exists():
				start_from_field_schema = FieldSchema.objects.get(name='startFrom')
			else:
				start_from_field_schema = FieldSchema.objects.create(name='startFrom', data_type='date')

			if FieldSchema.objects.filter(name='endTo').exists():
				end_to_field_schema = FieldSchema.objects.get(name='endTo')
			else:
				end_to_field_schema = FieldSchema.objects.create(name='endTo', data_type='date')

			userId = role_model_schema.add_field(user_id_field_schema, null=False, max_length=150)
			nodeId = role_model_schema.add_field(node_id_field_schema, max_length=150)
			startfrom = role_model_schema.add_field(start_from_field_schema, null=True)
			endto = role_model_schema.add_field(end_to_field_schema, null=True)


@receiver(post_save, sender=Base)
def fill_role_tables(sender, instance, created, **kwargs):
	if(UserRole.getObjectByUser(instance.userId)):
		userRole = UserRole.getObjectByUser(instance.userId)
		role_id_obj = userRole.roleId
		role_name = role_id_obj.roleName
		postFlag = role_id_obj.postFlag
		user_id = instance.userId.id
		node_id_of_base = instance.nodeId.nodeId
		role_id = role_id_obj.roleId
		node_id_of_role = get_node_id_of_role(node_id_of_base,role_id)
		if(postFlag==True):
			try:
				role_model_schema = ModelSchema.objects.get(name=role_name)
				roleTable = role_model_schema.as_model()
				if(roleTable.objects.filter(userid=user_id).exists()):
					# add startFrom and endTo fields
					roleTable.objects.get(userid=user_id).nodeid = node_id_of_role
				else:
					obj = roleTable.objects.create(userid=user_id,nodeid=node_id_of_role)
			except Exception as e:
				print(repr(e))


def get_node_id_of_role(node_id_of_base,role_id):
	level_role = len(role_id.split('.'))
	return '.'.join(node_id_of_base.split('.')[:level_role])


