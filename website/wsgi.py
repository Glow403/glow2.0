"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

def apply_migrations():
    """?????????????????????"""
    try:
        import django
        django.setup()
        from django.core.management import call_command
        call_command('migrate', '--run-syncdb', verbosity=0, stdout=open(os.devnull, 'w'))
    except Exception:
        pass

apply_migrations()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
