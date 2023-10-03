from loguru import logger
from pathlib import Path
from django.utils.http import urlquote
from django.http import FileResponse
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.buildhistory.models import BuildHistory
from application.buildhistory.serializers import BuildHistorySerializers

# Create your views here.


class BuildHistoryViewSets(viewsets.GenericViewSet):
    queryset = BuildHistory.objects.all()
    serializer_class = BuildHistorySerializers

    @action(methods=['get'], detail=False)
    def get_report(self, request, *args, **kwargs):
        logger.info('get log or report html file')
        history_id = request.query_params.get('id')
        file_type = request.query_params.get('type', 'log')
        if file_type == 'log':
            file_name = 'log.html'
        else:
            file_name = 'report.html'
        history = BuildHistory.objects.get(id=history_id)
        path = Path(history.report_path, file_name)
        if not path.is_file():
            return JsonResponse(code=10501, msg='file not found')
        # with open(file_path, 'rb') as f:
        #     file = f.read()
        file = open(path, 'rb', encoding='utf-8')
        response = FileResponse(file)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
        response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response
