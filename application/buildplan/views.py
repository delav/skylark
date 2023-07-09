from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.pagination.paginator import PagePagination
from infra.django.response import JsonResponse
from infra.utils.buildhandler import generate_task_name, convert_task_name
from application.usergroup.models import UserGroup
from application.user.models import User
from application.project.models import Project
from application.buildplan.models import BuildPlan
from application.buildplan.serializers import BuildPlanSerializers
from application.common.schedule.periodic import PeriodicHandler, get_periodic_task, get_periodic_list

# Create your views here.


class BuildPlanViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BuildPlan.objects.all()
    serializer_class = BuildPlanSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info(f'get build plan list: {request.query_params}')
        try:
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
            plan_list = []
            for item in pg_queryset:
                item_dict = self.get_serializer(item).data
                item_dict['periodic'] = get_periodic_task(id=item.periodic_task_id)
                plan_list.append(item_dict)
        except (Exception,) as e:
            logger.error(f'get plan list failed: {e}')
            return JsonResponse(code=10500, msg='get plan list failed')
        result = {'data': plan_list, 'total': queryset.count()}
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
            return JsonResponse(code=10501, msg='create build plan failed')
        result = self.get_serializer(plan).data
        result['periodic'] = get_periodic_task(id=plan.periodic_task_id)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update build plan: {request.data}')

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get build plan: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10502, msg='build info not found')
        result = self.get_serializer(instance).data
        result['periodic'] = get_periodic_task(id=instance.periodic_task_id)
        return JsonResponse(result)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete build plan: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete build plan error: {e}')
            return JsonResponse(code=10503, msg='delete build plan failed')
        return JsonResponse(data=instance.id)

    @action(methods=['get'], detail=False)
    def instantly(self, request, *args, **kwargs):
        logger.info(f'get instantly build plan')
        try:
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
        except (Exception,) as e:
            logger.error(f'get instantly build plan failed: {e}')
            return JsonResponse(code=10505, msg='get instantly build plan failed')
        return JsonResponse(data=result)



