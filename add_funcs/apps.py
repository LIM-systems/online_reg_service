from django.apps import AppConfig


class AddFuncsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'add_funcs'
    label = 'add_funcs'
    verbose_name = 'Дополнительное'

    def ready(self):
        import add_funcs.signals
