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
    # Auto-create admin user
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', '', 'admin123')
            print('Admin user created successfully')
    except Exception:
        pass

setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()