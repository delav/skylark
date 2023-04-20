from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.pagination.paginator import PagePagination
from application.infra.django.response import JsonResponse
from application.infra.utils.buildhandler import generate_task_name
from application.group.models import Group
from application.user.models import User
from application.project.models import Project
from application.buildplan.models import BuildPlan
from application.buildplan.serializers import BuildPlanSerializers
from application.common.schedule.periodic import PeriodicHandler, get_periodic_task

# Create your views here.


class BuildPlanViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BuildPlan.objects.all()
    serializer_class = BuildPlanSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info(f'get build plan list: {request.query_params}')
        groups_queryset = Group.objects.filter(user=request.user)
        users = User.objects.none()
        for group in groups_queryset:
            users |= group.user_set.all()
        group_emails = [user.email for user in users]
        projects = Project.objects.filter(create_by__in=group_emails, status=0)
        project_ids = [item.id for item in projects]
        queryset = self.get_queryset().filter(
            project_id__in=project_ids).order_by('-create_at')
        pg_queryset = self.paginate_queryset(queryset)
        result = []
        for item in pg_queryset:
            item_dict = self.get_serializer(item).data
            task_name = generate_task_name(item.id)
            item_dict['periodic'] = get_periodic_task(task_name)
            result.append(item_dict)
        return JsonResponse(data=result)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create build plan: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
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
        except (Exception,) as e:
            logger.error(f'create build plan failed: {e}')
            return JsonResponse(code=10100, msg='create build plan failed')
        result = self.get_serializer(plan).data
        task_name = generate_task_name(plan.id)
        result['periodic'] = get_periodic_task(task_name)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update build plan: {request.data}')

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get build plan: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10101, msg='build info not found')
        result = self.get_serializer(instance).data
        task_name = generate_task_name(instance.id)
        result['periodic'] = get_periodic_task(task_name)
        return JsonResponse(result)
