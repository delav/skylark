import os
import django
from .suitereader import SuiteContentReader

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skylark.settings")
django.setup()

