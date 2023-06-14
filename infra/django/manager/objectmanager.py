from django.db import models


class UserRelatedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'create_by', 'update_by'
        )
