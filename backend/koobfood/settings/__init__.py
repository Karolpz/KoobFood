import os

MODE = os.getenv('DJANGO_MODE', 'local')
if MODE == 'production':
    from .production import *
elif MODE == 'test':
    from .test import *
else:
    from .local import *