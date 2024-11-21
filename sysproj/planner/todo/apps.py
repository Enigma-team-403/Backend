from django.apps import AppConfig

class TodoConfig(AppConfig):
    name = 'todo'

    def ready(self):
        from . import tasks
        tasks.start()
