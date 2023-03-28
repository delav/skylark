import json
from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.infra.engine.dcsengine import DcsEngine
from application.buildplan.models import BuildPlan
from application.buildplan.serializers import BuildPlanSerializers
from application.timertask.serializers import TimerTaskSerializers
from application.common.parser.jsonparser import JsonParser
from application.common.schedule.timer import DynamicTimer

# Create your views here.


class BuildPlanViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = BuildPlan.objects.all()
    serializer_class = BuildPlanSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get build plan list: {request.query_params}')
        return JsonResponse(data={})

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create build plan: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.data['envs']
        project_id = serializer.data['project_id']
        project_name = serializer.data['project_name']
        run_data = serializer.data['run_data']
        common_struct, structure_list = JsonParser(project_id, project_name, env_id, run_data).parse()
        engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
        engine.init_common_data(common_struct)
        engine.visit(structure_list)
        batch_data = engine.get_batch_data()
        batch = len(batch_data)
        try:
            with transaction.atomic():
                instance = BuildPlan(
                    total_case=engine.get_case_count(),
                    create_by=request.user,
                    debug=serializer.data['debug'],
                    env_id=env_id,
                    project_id=project_id,
                    batch=batch,
                    build_data=json.dumps(batch_data)
                )
                instance.save()
                timer_info = serializer.data.get('timer_info')
                if not timer_info:
                    result = self.get_serializer(instance)
                    return JsonResponse(data=result.data)
                build_plan_id = instance.id
                timer_serializer = TimerTaskSerializers(data=timer_info)
                timer_serializer.is_valid(raise_exception=True)
                task_id_list = []
                for batch_no, data in batch_data.items():
                    suites, sources = data[0], data[1]
                    task_args = (str(build_plan_id), str(batch_no), suites, sources)
                    task_name = f'{build_plan_id}-{batch_no}'
                    periodic_id = DynamicTimer(
                        timer_str=timer_serializer['timer_str'],
                        timer_type=timer_serializer['timer_type']
                    ).save_task(task_name, settings.RUNNER_TASK, task_args, settings.RUNNER_QUEUE,
                                settings.RUNNER_ROUTING_KEY)
                    task_id_list.append(periodic_id)
                timer_serializer.save()
                instance.timer_task_id = timer_serializer.data['id']
                instance.save()
        except (Exception,) as e:
            logger.error(f'create build plan failed: {e}')
            return JsonResponse(code=10100, msg='create build plan failed')
        result = self.get_serializer(instance)
        return JsonResponse(data=result.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update build plan: {request.data}')

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get build plan: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10101, msg='build info not found')
        result = self.get_serializer(instance)
        return JsonResponse(result.data)
