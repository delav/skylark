from rest_framework import viewsets
from rest_framework.decorators import action


class InternalFileViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def download_file(self):
        pass
