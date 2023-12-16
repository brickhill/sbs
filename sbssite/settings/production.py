from .base import *


DEBUG = False
ALLOWED_HOSTS = ["http://whitchurch.pythonanywhere.com",
"whitchurch.pythonanywhere.com",
"http://www.sbsys.co.uk",
"www.sbsys.co.uk"]

try:
    from .local import *
except ImportError:
    pass
