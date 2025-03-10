from django.apps import AppConfig


class apiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import signals
        return super().ready()