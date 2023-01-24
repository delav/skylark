import os
import django

# register to django apps
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skylark.settings")
django.setup()
