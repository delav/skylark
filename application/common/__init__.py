import os
import django
from application.common.keyword import init_lib_keyword_cache, init_user_keyword_cache

# register to django apps
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skylark.settings")
django.setup()

init_lib_keyword_cache()
init_user_keyword_cache()
