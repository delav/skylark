from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.builder.models import Builder
from application.builder.serializers import BuilderSerializers
from application.common.reader.structure import Structure


# Create your views here.


class BuilderViewSets(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get build list: {request.query_params}')
        return JsonResponse(data={})

    def create(self, request, *args, **kwargs):
        logger.info(f'create build: {request.data}')
        root = request.data.get('data')
        project_id = root.get('mid')
        project_name = root.get('name')
        data = Structure(project_id, project_name).parser_from_db()
        # Runner(data).start()
        return JsonResponse(data={'build_id': 1})

    def retrieve(self, request, *args, **kwargs):
        pass


