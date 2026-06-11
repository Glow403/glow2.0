import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

def setup():
    import django
    django.setup()
    try:
        from django.core.management import call_command
        call_command('migrate', '--run-syncdb', verbosity=0)
    except Exception:
        pass

setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()