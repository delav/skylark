from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.project.models import Project
from application.common.handler import fill_node

# Create your views here.


class SuiteDirViewSets(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SuiteDir.objects.all()
    serializer_class = SuiteDirSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project base dir by project id: {request.query_params}')
        try:
            project_id = request.query_params.get('project')
            project = Project.objects.get(id=project_id)
        except (Exception,) as e:
            logger.error(f'get base dir info failed: {e}')
            return JsonResponse(code=10052, msg='get base dir failed')
        dirs = project.dirs.filter(parent_dir=None).order_by('dir_type')
        project_tree_list = []
        project_node = fill_node(
            {'id': project.id, 'pId': 0, 'name': project.name, 'desc': 'p', 'type': 0}
        )
        project_tree_list.append(project_node)
        for d in dirs.iterator():
            dir_node = fill_node(
                {'id': d.id, 'pId': project.id, 'name': d.dir_name, 'desc': 'd', 'type': d.dir_type},
            )
            project_tree_list.append(dir_node)
        return JsonResponse(data=project_tree_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create suite dir: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except (Exception,) as e:
            logger.error(f'save suite dir failed: {e}')
            return JsonResponse(code=10060, msg='create suite dir failed')
        return JsonResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
