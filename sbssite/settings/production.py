from .base import *

DEBUG = False
ALLOWED_HOSTS = ["http://whitchurch.pythonanywhere.com"]
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY") if "DJANGO_SECRET_KEY" in os.environ else ""
try:
    from .local import *
except ImportError:
    pass
