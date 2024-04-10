from django.apps import AppConfig


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api_apec'
    def ready(self):
        from apps.api_apec import updater
        updater.start()

