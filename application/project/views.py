from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.user.models import User
from application.group.models import Group
from application.infra.common import PagePagination
from application.infra.response import JsonResponse
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.common.replicator import ProjectReplicator

# Create your views here.


class ProjectViewSets(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info('get project list by current user')
        gps = Group.objects.filter(user=request.user)
        gp_users = User.objects.none()
        for gp in gps:
            gp_users |= gp.user_set.all()
        queryset = Project.objects.filter(create_by__in=gp_users)
        pg_queryset = self.paginate_queryset(queryset)
        ser = self.get_serializer(pg_queryset, many=True)
        return JsonResponse(data=ser.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create project: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # test
        self.perform_create(serializer)
        # data = serializer.data
        # project_name = data.get('name')
        # project_q = Project.objects.filter(name=project_name)
        # if project_q.exists():
        #     return JsonResponse(code=10080, data='project name had exists')
        # try:
        #     if 'copy_pid' in data:
        #         copy_pid = data.get('copy_pid')
        #         copy_project = Project.objects.get(id=copy_pid)
        #     else:
        #         module_name = settings.PROJECT_MODULE_ID
        #         copy_project = Project.objects.get(name=module_name)
        # except (Exception,) as e:
        #     logger.error(f'project module not exists: {e}')
        #     return JsonResponse(code=10051, data='create project failed')
        # logger.info(f'copied project: {copy_project.name}')
        # try:
        #     with transaction.atomic():
        #         project = ProjectReplicator(copy_project, request.user).project_copy()
        # except Exception as e:
        #     logger.error(f'create project error: {e}')
        #     # database rollback
        #     transaction.savepoint_rollback(save_id)
        #     return JsonResponse(code=10081, msg='create project failed')
        return JsonResponse(data={'project_id': project.id, 'name': project.name})

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        logger.info(f'update project: {request.data}')

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete project: {kwargs.get("pk")}')


class AdminProjectViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    pagination_class = PagePagination
