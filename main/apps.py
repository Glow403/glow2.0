from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        try:
            from django.core.management import call_command
            call_command('migrate', '--run-syncdb', verbosity=0)
        except Exception:
            pass
