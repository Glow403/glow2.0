import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

def setup():
    import django
    django.setup()
    try:
        from django.core.management import call_command
        call_command("migrate", verbosity=0)
        print("Migrations applied successfully", flush=True)
    except Exception as e:
        print(f"Migrate error: {e}", flush=True)
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "", "admin123")
            print("Admin created", flush=True)
    except Exception as e:
        print(f"Admin error: {e}", flush=True)

setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
