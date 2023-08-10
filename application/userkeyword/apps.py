from django.apps import AppConfig
from application.storage import load_user_keyword_to_storage


class UserKeywordConfig(AppConfig):
    name = 'application.userkeyword'

    def ready(self):
        from .models import UserKeyword
        load_user_keyword_to_storage(UserKeyword)
