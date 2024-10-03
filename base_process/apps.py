from django.apps import AppConfig


class BaseProcessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_process'
    label = 'base_process'
    verbose_name = 'Основное'

    def ready(self):
        import base_process.signals
