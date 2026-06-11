import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

try:
    django.setup()
    from django.core.management import call_command
    call_command('collectstatic', '--noinput', verbosity=0)
except Exception as e:
    print(f"Warning: collectstatic failed: {e}", file=sys.stderr)

bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
workers = 2
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
