from django.apps import AppConfig


class MuseumAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'museum_app'

    def ready(self):
        import museum_app.signals
