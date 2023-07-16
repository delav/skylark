import os
import django
from application.common.keyword import init_lib_keyword, init_user_keyword

# register to django apps
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skylark.settings")
django.setup()

init_lib_keyword()
init_user_keyword()
