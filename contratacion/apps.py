from django.apps import AppConfig

class ContratacionConfig(AppConfig):
    name = 'contratacion'

    def ready(self):
        import contratacion.signals 