from django.apps import AppConfig
from django.db import connection
from application.storage import load_lib_keyword_to_storage


class LibKeywordConfig(AppConfig):
    name = 'application.libkeyword'

    def ready(self):
        from .models import LibKeyword
        with connection.cursor() as cursor:
            table_names = connection.introspection.table_names()
            if LibKeyword._meta.db_table not in table_names:
                return
        load_lib_keyword_to_storage(LibKeyword)
