from django.db import connection


class AutoMigrateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        try:
            connection.ensure_connection()
            from django.core.management import call_command
            call_command('migrate', '--run-syncdb', verbosity=0)
        except Exception:
            pass
        return None
