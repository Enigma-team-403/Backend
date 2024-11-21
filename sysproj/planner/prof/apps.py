from django.apps import AppConfig

class ProfConfig(AppConfig):
    name = 'prof'

    def ready(self):
        import prof.signals
