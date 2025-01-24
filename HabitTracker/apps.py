from django.apps import AppConfig

class HabitTrackerConfig(AppConfig):
    name = 'HabitTracker'

    def ready(self):
        import HabitTracker.signals  # اطمینان از متصل شدن سیگنال‌ها
