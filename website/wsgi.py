import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

print("=" * 60, flush=True)
print("DEPLOY_ID: 2026-06-12-final-admin-fix-v2", flush=True)
print("=" * 60, flush=True)

def setup():
    import django
    django.setup()
    try:
        from django.db import connection
        connection.ensure_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        print("Database connected OK", flush=True)
    except Exception as e:
        print(f"Database FAILED: {e}", flush=True)
        raise
    try:
        from django.contrib.admin import site
        print("Admin loaded OK", flush=True)
    except Exception as e:
        print(f"Admin FAILED: {e}", flush=True)
        raise
    try:
        from django.core.management import call_command
        call_command("migrate", verbosity=0)
        print("Migrations OK", flush=True)
    except Exception as e:
        print(f"Migrate error: {e}", flush=True)
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "", "admin123")
    except Exception as e:
        print(f"Admin error: {e}", flush=True)
    print("Setup complete", flush=True)

setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
print("WSGI application ready", flush=True)
