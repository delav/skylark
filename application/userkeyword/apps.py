from django.apps import AppConfig
from django.db import connection
from application.storage import load_user_keyword_to_storage


class UserKeywordConfig(AppConfig):
    name = 'application.userkeyword'

    def ready(self):
        from .models import UserKeyword
        with connection.cursor() as cursor:
            table_names = connection.introspection.table_names()
            if UserKeyword._meta.db_table not in table_names:
                return
        load_user_keyword_to_storage(UserKeyword)
