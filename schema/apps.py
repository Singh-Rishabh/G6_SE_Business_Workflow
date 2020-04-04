from django.apps import AppConfig


class SchemaConfig(AppConfig):
    name = 'schema'

    def ready(self):
        import schema.signals
