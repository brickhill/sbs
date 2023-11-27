from .base import *

DEBUG = False
ALLOWED_HOSTS = ["http://whitchurch.pythonanywhere.com"]

try:
    from .local import *
except ImportError:
    pass
