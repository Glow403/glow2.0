import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from django.contrib.auth.models import User

try:
    admin = User.objects.get(username="admin")
    print("admin user already exists")
except User.DoesNotExist:
    User.objects.create_superuser("admin", "", "admin123")
    print("admin created successfully, password: admin123")
