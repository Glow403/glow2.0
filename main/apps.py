from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        # Import signals to connect them
        import main.models  # noqa: F401
