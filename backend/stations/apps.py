from django.apps import AppConfig


class StationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stations'
    verbose_name = 'Радиостанции'

    def ready(self):
        import stations.signals
