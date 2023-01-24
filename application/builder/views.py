import datetime
import os
from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.builder.models import Builder
from application.builder.serializers import BuilderSerializers, BuildDataSerializers
from application.common.reader.parser import DBParser, JsonParser
from skylark.celeryapp import app

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
        serializer = BuildDataSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        online = serializer.data['online']
        env_id = serializer.data['env']
        project_id = serializer.data['project_id']
        project_name = serializer.data['project_name']
        run_data = serializer.data['run_data']
        try:
            instance = Builder(
                build_by=request.user,
                cron_job=serializer.data['cron_job'],
                debug=serializer.data['debug'],
                env_id=env_id,
                project_id=project_id
            )
            instance.save()
        except (Exception,) as e:
            logger.error(f'build task failed: {e}')
            return JsonResponse(code=10100, msg='build task failed')
        if online:
            data, suites = JsonParser(project_id, project_name, run_data, env_id).parser()
        else:
            data, suites = DBParser(project_id, project_name, run_data, env_id).parser()
        build_id = str(instance.id)
        metadata = {'taskid': build_id, 'data': data}
        report_path = os.path.join(settings.REPORT_PATH, project_name, build_id)
        app.send_task('task.tasks.robot_runner',
                      queue='runner',
                      args=(build_id, suites, metadata, report_path)
                      )
        return JsonResponse(data={'build_id': build_id})

    def retrieve(self, request, *args, **kwargs):
        pass


