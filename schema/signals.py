from django.db.models.signals import post_save
from django.dispatch import receiver
from schema.models import RoleHierarchy, ModelSchema, FieldSchema


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

			if FieldSchema.objects.filter(name='startfrom').exists():
				start_from_field_schema = FieldSchema.objects.get(name='startfrom')
			else:
				start_from_field_schema = FieldSchema.objects.create(name='startfrom', data_type='date')

			if FieldSchema.objects.filter(name='endto').exists():
				end_to_field_schema = FieldSchema.objects.get(name='endto')
			else:
				end_to_field_schema = FieldSchema.objects.create(name='endto', data_type='date')

			userId = role_model_schema.add_field(user_id_field_schema, null=False, max_length=150)
			nodeId = role_model_schema.add_field(node_id_field_schema, max_length=150)
			startfrom = role_model_schema.add_field(start_from_field_schema)
			endto = role_model_schema.add_field(end_to_field_schema)






