from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.pagination.paginator import PagePagination
from infra.django.response import JsonResponse
from application.builder.handler import generate_task_name, convert_task_name
from application.usergroup.models import UserGroup
from application.user.models import User
from application.project.models import Project
from application.buildplan.models import BuildPlan
from application.buildplan.serializers import BuildPlanSerializers
from application.common.scheduler.periodic import PeriodicHandler, get_periodic_task, get_periodic_list

# Create your views here.


class BuildPlanViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BuildPlan.objects.all()
    serializer_class = BuildPlanSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info(f'get build plan list: {request.query_params}')
        project_id = request.query_params.get('project')
        groups_queryset = UserGroup.objects.filter(user=request.user)
        users = User.objects.none()
        for group in groups_queryset:
            users |= group.user_set.all()
        group_emails = [user.email for user in users]
        projects = Project.objects.filter(create_by__in=group_emails, status=0)
        project_ids = [item.id for item in projects]
        if project_id:
            queryset = self.get_queryset().filter(
                project_id=project_id).order_by('-create_at')
        else:
            queryset = self.get_queryset().filter(
                project_id__in=project_ids).order_by('-create_at')
        pg_queryset = self.paginate_queryset(queryset)
        plan_list = self.get_serializer(pg_queryset, many=True).data
        result = {'data': plan_list, 'total': queryset.count()}
        return JsonResponse(data=result)

    def create(self, request, *args, **kwargs):
        logger.info(f'create build plan: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            valid_data = serializer.validated_data
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
                settings.PERIODIC_QUEUE,
                settings.PERIODIC_ROUTING_KEY
            )
            plan.periodic_task_id = periodic_task_id
            plan.save()
        result = self.get_serializer(plan).data
        result['periodic'] = get_periodic_task(id=plan.periodic_task_id)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update build plan: {request.data}')

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get plan detail: {kwargs.get("pk")}')
        instance = self.get_object()
        result = self.get_serializer(instance).data
        result['periodic'] = get_periodic_task(id=instance.periodic_task_id)
        return JsonResponse(result)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete build plan: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)

    @action(methods=['get'], detail=False)
    def get_instantly_plan_list(self, request, *args, **kwargs):
        logger.info(f'get instantly build plan')
        limit = request.query_params.get('limit')
        periodic_list = get_periodic_list(enabled=True)
        sort_periodics = sorted(periodic_list, key=lambda o: o['to_next'], reverse=False)
        plan_id_list = []
        periodic_dict = {}
        min_length = min(len(sort_periodics), int(limit))
        for i in range(min_length):
            periodic = sort_periodics[i]
            plan_id = convert_task_name(periodic.get('name'))
            plan_id_list.append(plan_id)
            periodic_dict[plan_id] = periodic
        queryset = BuildPlan.objects.filter(id__in=plan_id_list)
        result = []
        for item in queryset.iterator():
            data = self.get_serializer(item).data
            data['periodic'] = periodic_dict[item.id]
            result.append(data)
        return JsonResponse(data=result)



