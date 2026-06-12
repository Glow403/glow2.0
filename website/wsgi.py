import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

application = get_wsgi_application()
static_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "staticfiles")
if os.path.isdir(static_root):
    application = WhiteNoise(application, root=static_root, prefix="/static/")
