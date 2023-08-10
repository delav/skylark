from django.apps import AppConfig
from application.storage import load_lib_keyword_to_storage


class LibKeywordConfig(AppConfig):
    name = 'application.libkeyword'

    def ready(self):
        from .models import LibKeyword
        load_lib_keyword_to_storage(LibKeyword)
