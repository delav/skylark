from pathlib import Path
from io import StringIO
from re import search
from loguru import logger
from django.db import transaction
from django.utils.http import urlquote
from django.http import FileResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from infra.utils.timehanldler import get_timestamp
from application.constant import ModuleCategory, ModuleStatus, FileSaveMode
from application.suitedir.models import SuiteDir
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.virtualfile.models import VirtualFile
from application.virtualfile.serializers import VirtualFileSerializers, UploadForm
from application.common.ztree.generatenode import handler_suite_node
from application.virtualfile.handler import PATH_SEPARATOR, get_file_content, get_full_dir_path

# Create your views here.


class VirtualFileViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def save_content(self, request, *args, **kwargs):
        logger.info(f'create file: {request.data}')
        serializer = VirtualFileSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_data = serializer.validated_data
        suite_id = file_data.get('suite_id')
        suite_query = TestSuite.objects.filter(
            id=suite_id,
            category=ModuleCategory.VARIABLE,
            status=ModuleStatus.NORMAL
        )
        if not suite_query.exists():
            return JsonResponse(code=10307, msg='not found')
        suite_dir = suite_query.first().suite_dir
        full_path_list = get_full_dir_path(suite_dir, [])
        file_name = suite_query.first().name
        suffix = str(search(r'\w*(.\w*)', file_name).group(1))
        file_data['file_name'] = file_name
        file_data['file_suffix'] = suffix
        file_data['update_time'] = int(get_timestamp(10))
        file_data['edit_file'] = True
        file_data['file_path'] = PATH_SEPARATOR.join(full_path_list)
        print(file_data)
        if suffix not in settings.VARIABLE_FILE_TYPE:
            return JsonResponse(code=10308, msg='file type not supported')
        instance, _ = VirtualFile.objects.update_or_create(
            suite_id=file_data.get('suite_id'),
            defaults=file_data
        )
        data = VirtualFileSerializers(instance).data
        return JsonResponse(data=data)

    @action(methods=['get'], detail=False)
    def get_content(self, request, *args, **kwargs):
        logger.info(f'get file content by suite id: {request.query_params}')
        suite_id = request.query_params.get('suite')
        suite_query = TestSuite.objects.filter(
            id=suite_id
        )
        if not suite_query.exists():
            return JsonResponse(code=10307, msg='not found')
        suite = suite_query.first()
        if suite.status == ModuleStatus.DELETED:
            return JsonResponse(code=10307, msg='file not found')
        data = get_file_content(suite_id)
        default = {
            'env_id': None,
            'region_id': None,
            'file_path': '',
            'file_name': suite.name,
            'file_suffix': str(search(r'\w*(.\w*)', suite.name).group(1)),
            'file_text': '',
            'suite_id': suite.id,
            'edit_file': True
        }
        data = data or default
        return JsonResponse(data=data)


class ProjectFileViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def upload(self, request, *args, **kwargs):
        logger.info(f'upload files')
        form = UploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse(code=10302, msg='upload failed')
        files = request.FILES.getlist('file')
        node_list = []
        dir_id = form.cleaned_data.get('dir_id')
        dir_queryset = SuiteDir.objects.filter(
            id=dir_id,
            category=ModuleCategory.FILE,
            status=ModuleStatus.NORMAL
        )
        if not dir_queryset.exists():
            return JsonResponse(code=10303, msg='dir not found')
        dir_path = get_full_dir_path(dir_queryset.first(), [])
        with transaction.atomic():
            for f in files:
                if f.size > settings.FILE_SIZE_LIMIT:
                    continue
                suffix = str(search(r'\w*(.\w*)', f.name).group(1))
                related_suite_data = {
                    'name': f.name,
                    'category': ModuleCategory.FILE,
                    'suite_dir_id': dir_id
                }
                serializer = TestSuiteSerializers(data=related_suite_data)
                serializer.is_valid(raise_exception=True)
                validate_data = serializer.validated_data
                validate_data['create_by'] = request.user.email
                suite, created = TestSuite.objects.update_or_create(
                    name=validate_data.get('name'),
                    suite_dir_id=validate_data.get('suite_dir_id'),
                    defaults=validate_data
                )
                file_path = Path(settings.PROJECT_FILES, *dir_path)
                if f.size > settings.SAVE_TO_DB_SIZE_LIMIT or suffix not in settings.SAVE_TO_DB_FILE_TYPE:
                    save_mode = FileSaveMode.FILE
                    file_text = None
                    self.save_file_to_disk(file_path, f)
                else:
                    save_mode = FileSaveMode.DB
                    file_text = f.read()
                if created:
                    VirtualFile.objects.create(
                        suite_id=suite.id,
                        file_path=PATH_SEPARATOR.join(dir_path),
                        file_name=f.name,
                        file_suffix=suffix,
                        save_mode=save_mode,
                        file_text=file_text,
                        update_time=int(get_timestamp(10))
                    )
                else:
                    file_obj = VirtualFile.objects.get(suite_id=suite.id)
                    file_obj.status = ModuleStatus.NORMAL
                    file_obj.save_mode = save_mode
                    file_obj.file_text = file_text
                    file_obj.update_time = int(get_timestamp(10))
                    file_obj.save()
                suite_data = TestSuiteSerializers(suite).data
                suite_data['extra_data'] = {}
                node_list.append(handler_suite_node(suite_data))
        return JsonResponse(data=node_list)

    @action(methods=['post'], detail=False)
    def download(self, request, *args, **kwargs):
        logger.info(f'download file')
        suite_id = request.POST.get('suite')
        instance = VirtualFile.objects.get(suite_id=suite_id)
        if instance.status == ModuleStatus.DELETED:
            return JsonResponse(code=100308, msg='file not exist')
        child_path_list = instance.file_path.split(PATH_SEPARATOR)
        file_path = Path(settings.PROJECT_FILES, *child_path_list)
        file_name = instance.file_name
        file = None
        if instance.save_mode == FileSaveMode.FILE:
            file = self.read_file_from_dick(file_path, file_name)
        elif instance.save_mode == FileSaveMode.DB:
            file = StringIO()
            file.write(instance.file_text)
        if file is None:
            return JsonResponse(code=10304, msg='file not exist')
        response = FileResponse(file)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
        response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response

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
        return open(file, 'rb', encoding='utf-8')
