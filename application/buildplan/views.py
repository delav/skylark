from loguru import logger
from django.conf import settings
from django.db import transaction, IntegrityError
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.pagination.paginator import PagePagination
from infra.django.response import JsonResponse
from application.constant import ModuleStatus
from application.manager import get_projects_by_uid
from application.builder.handler import generate_task_name, convert_task_name
from application.projectpermission.models import ProjectPermission
from application.project.models import Project
from application.buildplan.models import BuildPlan
from application.buildplan.serializers import BuildPlanSerializers
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers
from application.common.scheduler.periodic import PeriodicHandler, get_periodic_task, get_periodic_list
from application.common.access.projectaccess import has_project_permission

# Create your views here.


class BuildPlanViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BuildPlan.objects.all()
    serializer_class = BuildPlanSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info(f'get build plan list: {request.query_params}')
        project_id = request.query_params.get('project_id')
        if project_id:
            if not project_id.isdigit():
                return JsonResponse(code=40309, msg='Param error')
            if not has_project_permission(project_id, request.user):
                return JsonResponse(code=40300, msg='403_FORBIDDEN')
            queryset = self.get_queryset().filter(
                status=ModuleStatus.NORMAL,
                project_id=project_id).order_by('-create_at')
        else:
            project_list = get_projects_by_uid(request.user.id)
            project_ids = [item.get('id') for item in project_list]
            queryset = self.get_queryset().filter(
                status=ModuleStatus.NORMAL,
                project_id__in=project_ids).order_by('-create_at')
        create_by = request.query_params.get('create_by')
        if create_by:
            queryset = queryset.filter(create_by=create_by)
        pg_queryset = self.paginate_queryset(queryset)
        plan_list = self.get_serializer(pg_queryset, many=True).data
        result = {'data': plan_list, 'total': queryset.count()}
        return JsonResponse(data=result)

    def create(self, request, *args, **kwargs):
        logger.info(f'create build plan: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        project_id = valid_data.get('project_id')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40301, msg='403_FORBIDDEN')
        with transaction.atomic():
            plan = BuildPlan.objects.create(**valid_data)
            plan_id = plan.id
            periodic_expr = valid_data.get('periodic_expr', '')
            if not valid_data.get('periodic_switch'):
                result = self.get_serializer(plan).data
                result['periodic'] = {}
                return JsonResponse(data=result)
            task_name = generate_task_name(plan_id)
            periodic_handler = PeriodicHandler(periodic_expr)
            periodic_task_id = periodic_handler.save_task(
                task_name,
                settings.PERIODIC_TASK,
                str(plan_id),
                settings.BUILDER_QUEUE,
                settings.BUILDER_ROUTING_KEY
            )
            plan.periodic_task_id = periodic_task_id
            plan.save()
        result = self.get_serializer(plan).data
        result['periodic'] = get_periodic_task(id=plan.periodic_task_id)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update build plan: {request.data}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except IntegrityError:
            return JsonResponse(code=40302, msg='update dir name already exist')
        return JsonResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get plan detail: {kwargs.get("pk")}')
        instance = self.get_object()
        result = self.get_serializer(instance).data
        result['periodic'] = get_periodic_task(id=instance.periodic_task_id)
        result['record'] = []
        queryset = BuildRecord.objects.filter(
                plan_id=instance.id).order_by('-create_at')[:5]
        if queryset.exists():
            records = BuildRecordSerializers(queryset, many=True).data
            result['record'] = records
        return JsonResponse(result)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete build plan: {kwargs.get("pk")}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        instance.status = ModuleStatus.DELETED
        instance.update_by = request.user.email
        instance.save()
        return JsonResponse(data=instance.id)

    @action(methods=['get'], detail=False)
    def get_instantly_plan_list(self, request, *args, **kwargs):
        logger.info(f'get instantly build plan')
        limit = request.query_params.get('limit')
        periodic_list = get_periodic_list(enabled=True)
        plan_id_list = []
        periodic_dict = {}
        min_length = min(len(periodic_list), int(limit))
        for i in range(min_length):
            periodic = periodic_list[i]
            plan_id = convert_task_name(periodic.get('name'))
            plan_id_list.append(plan_id)
            periodic_dict[plan_id] = periodic
        queryset = BuildPlan.objects.filter(
            status=ModuleStatus.NORMAL,
            id__in=plan_id_list
        )
        result = []
        for item in queryset.iterator():
            data = self.get_serializer(item).data
            data['periodic'] = periodic_dict[item.id]
            result.append(data)
        sort_result = sorted(result, key=lambda o: o['periodic']['to_next'], reverse=False)
        return JsonResponse(data=sort_result)



