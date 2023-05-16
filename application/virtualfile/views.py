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
from application.infra.django.response import JsonResponse
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.virtualfile.models import VirtualFile
from application.virtualfile.serializers import VirtualFileSerializers, UploadForm

# Create your views here.


class VirtualFileViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = VirtualFile.objects.all()
    serializer_class = VirtualFileSerializers

    def create(self, request, *args, **kwargs):
        logger.info('create file')

    def list(self, request, *args, **kwargs):
        logger.info(f'get virtual file by suite id: {request.query_params}')
        try:
            suite_id = request.query_params.get('suite')
            queryset = self.queryset.filter(suite_id=suite_id)
            if not queryset.exists():
                return JsonResponse(data={})
            serializer = self.get_serializer(queryset.first())
            return JsonResponse(data=serializer.data)
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
            success_count = 0
            with transaction.atomic():
                for f in files:
                    if f.size > settings.FILE_SIZE_LIMIT:
                        continue
                    subfix = str(search(r'\w*(.\w*)', f.name).group(1))
                    suite_data = {
                        'name': f.name,
                        'category': settings.CATEGORY_META.get('ProjectFile'),
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
                    suite_id = suites[0].id
                    child_path = form.cleaned_data.get('path')
                    child_path_list = child_path.split('/')
                    file_path = Path(settings.PROJECT_FILES, *child_path_list)
                    self.save_file_to_disk(file_path, f)
                    VirtualFile.objects.update_or_create(
                        suite_id=suite_id,
                        file_path=child_path,
                        file_subfix=subfix,
                        defaults={'file_text': f.chunks()}
                    )
                    success_count += 1
        except Exception as e:
            logger.error(f'upload failed: {e}')
            return JsonResponse(code=10303, msg='upload failed')
        return JsonResponse(data=success_count)

    @action(methods=['post'], detail=False)
    def download(self, request, *args, **kwargs):
        logger.info(f'download file: {request.form}')
        file_info = VirtualFile.objects.get(id=id)
        file = open(file_info.file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment;filename="{urlquote(file_info.file_name)}"'
        return response

    @staticmethod
    def save_file_to_disk(file_path, f):
        Path(file_path).mkdir(parents=True, exist_ok=True)
        file = file_path / f.name
        destination = open(file, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
