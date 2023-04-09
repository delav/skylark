from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.user.models import User
from application.group.models import Group
from application.infra.django.pagination.paginator import PagePagination
from application.infra.django.response import JsonResponse
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.common.operator import ProjectOperator

# Create your views here.


class ProjectViewSets(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get project list by current user')
        groups_queryset = Group.objects.filter(user=request.user)
        users = User.objects.none()
        for group in groups_queryset:
            users |= group.user_set.all()
        group_emails = [user.email for user in users]
        queryset = Project.objects.filter(create_by__in=group_emails, status=0)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create project: {request.data}')
        cname = request.data.get('cname')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_name = serializer.data.get('name')
        project_q = Project.objects.filter(name=project_name)
        if project_q.exists():
            return JsonResponse(code=10080, data='project name already exists')
        default_project_name = settings.PROJECT_MODULE
        copied_project_name = cname or default_project_name
        try:
            copied_project = Project.objects.get(name=copied_project_name)
            operator = ProjectOperator(project_name, copied_project, request.user)
            with transaction.atomic():
                operator.copy_project_action() if cname else operator.new_project_action()
                project = operator.get_new_project()
        except (Exception,) as e:
            logger.error(f'create project error: {e}')
            return JsonResponse(code=10081, msg='create project failed')
        logger.info(f'copied project: {copied_project_name}')
        result_serializer = self.get_serializer(project)
        return JsonResponse(data=result_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        logger.info(f'update project: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except (Exception,) as e:
            logger.error(f'update project failed: {e}')
            return JsonResponse(code=10087, msg='update project failed')
        return JsonResponse(serializer.data)


class AdminProjectViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info('get project list by admin')
        queryset = self.get_queryset()
        pg_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pg_queryset, many=True)
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete project by admin: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete project error: {e}')
            return JsonResponse(code=10086, msg='delete project failed')
        return JsonResponse(data=instance.id)