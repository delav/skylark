from pathlib import Path
from re import search
from loguru import logger
from django.db import transaction
from django.utils.http import urlquote
from django.http import FileResponse
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.constant import CATEGORY_META
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.virtualfile.models import VirtualFile
from application.virtualfile.serializers import VirtualFileSerializers, UploadForm
from application.common.ztree.generatenode import handler_suite_node
from application.common.handler.filedatahandler import get_file_content

# Create your views here.


class VirtualFileViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = VirtualFile.objects.all()
    serializer_class = VirtualFileSerializers

    def create(self, request, *args, **kwargs):
        logger.info('create file')

    def list(self, request, *args, **kwargs):
        logger.info(f'get file content by suite id: {request.query_params}')
        try:
            suite_id = request.query_params.get('suite')
            data = get_file_content(suite_id)
            return JsonResponse(data=data)
        except (Exception,) as e:
            logger.error(f'get virtual file failed: {e}')
            return JsonResponse(code=10301, msg='get virtual file failed')


class FileViewSets(viewsets.GenericViewSet):

    @transaction.atomic
    @action(methods=['post'], detail=False)
    def upload(self, request, *args, **kwargs):
        logger.info(f'upload files')
        form = UploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse(code=10302, msg='upload failed')
        files = request.FILES.getlist('file')
        try:
            node_list = []
            with transaction.atomic():
                for f in files:
                    if f.size > settings.FILE_SIZE_LIMIT:
                        continue
                    subfix = str(search(r'\w*(.\w*)', f.name).group(1))
                    suite_data = {
                        'name': f.name,
                        'category': CATEGORY_META.get('ProjectFile'),
                        'suite_dir_id': form.cleaned_data.get('dir_id')
                    }
                    serializer = TestSuiteSerializers(data=suite_data)
                    serializer.is_valid(raise_exception=True)
                    validate_data = serializer.data
                    validate_data['create_by'] = request.user.email
                    suites = TestSuite.objects.update_or_create(
                        name=validate_data.get('name'),
                        suite_dir_id=validate_data.get('suite_dir_id'),
                        defaults=validate_data
                    )
                    suite = suites[0]
                    child_path = form.cleaned_data.get('path')
                    child_path_list = child_path.split('/')
                    file_path = Path(settings.PROJECT_FILES, *child_path_list)
                    self.save_file_to_disk(file_path, f)
                    VirtualFile.objects.update_or_create(
                        suite_id=suite.id,
                        file_path=child_path,
                        file_name=f.name,
                        file_subfix=subfix,
                        defaults={'file_text': f.chunks()}
                    )
                    suite_data = TestSuiteSerializers(suite).data
                    suite_data['extra_data'] = {}
                    node_list.append(handler_suite_node(suite_data))
        except Exception as e:
            logger.error(f'upload failed: {e}')
            return JsonResponse(code=10303, msg='upload failed')
        return JsonResponse(data=node_list)

    @action(methods=['post'], detail=False)
    def download(self, request, *args, **kwargs):
        logger.info(f'download file')
        suite_id = request.POST.get('suite')
        try:
            instance = VirtualFile.objects.get(suite_id=suite_id)
            child_path_list = instance.file_path.split('/')
            file_path = Path(settings.PROJECT_FILES, *child_path_list)
            file_name = instance.file_name
            file = self.read_file_from_dick(file_path, file_name)
            if file is None:
                return JsonResponse(code=10304, msg='file not exist')
            response = FileResponse(file)
            response['Content-Type'] = "application/octet-stream"
            response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
            response['Access-Control-Expose-Headers'] = "Content-Disposition"
            return response
        except (Exception,) as e:
            logger.error(f'download file failed: {e}')
            return JsonResponse(code=10305, msg='download failed')

    @staticmethod
    def save_file_to_disk(file_path, f):
        Path(file_path).mkdir(parents=True, exist_ok=True)
        file = file_path / f.name
        destination = open(file, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

    @staticmethod
    def read_file_from_dick(file_path, file_name):
        file = Path(file_path, file_name)
        if not file.exists():
            return None
        return open(file, 'rb')
