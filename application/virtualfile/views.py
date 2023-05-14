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
        print("POST DATA: ", request.FILES)
        form = UploadForm(request.POST)
        if not form.is_valid():
            return JsonResponse(code=10302, msg='upload failed')
        files = request.FILES.getlist('file')
        logger.info(f'files:', files)
        try:
            with transaction.atomic():
                for f in files:
                    if f.size > 10 * 1024:
                        continue
                    subfix = str(search(r'\w*(.\w*)', f.name).group(1))
                    suite_data = {
                        'name': f.name,
                        'category': settings.CATEGORY_META.get('ProjectFile'),
                        'suite_dir_id': form.dir_id
                    }
                    serializer = TestSuiteSerializers(data=suite_data)
                    serializer.is_valid(raise_exception=True)
                    suite = TestSuite.objects.create(**serializer.data)
                    VirtualFile.objects.create(
                        suite_id=suite.id,
                        file_subfix=subfix,
                        file_text=f.chunks()
                    )
                    file_path = settings.PROJECT_FILE / form.path / f.name
                    destination = open(file_path, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    destination.close()
        except Exception as e:
            logger.error(f'upload failed: {e}')
            return JsonResponse(code=10303, msg='upload failed')
        return JsonResponse()

    @action(methods=['post'], detail=False)
    def download(self, request, *args, **kwargs):
        logger.info(f'register user: {request.form}')
        file_info = VirtualFile.objects.get(id=id)
        file = open(file_info.file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment;filename="{urlquote(file_info.file_name)}"'
        return response
