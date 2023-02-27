from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.projectversion.models import ProjectVersion
from application.projectversion.serializers import ProjectVersionSerializers

# Create your views here.


class ProjectVersionViewSets(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ProjectVersion.objects.all()
    serializer_class = ProjectVersionSerializers

    def retrieve(self, request, *args, **kwargs):
        pass

