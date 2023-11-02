from pathlib import Path
from io import StringIO
from re import search
from loguru import logger
from django.db import transaction
from django.utils.http import urlquote
from django.http import FileResponse, HttpResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from infra.crypto.crypter import base64_encrypt
from infra.utils.timehanldler import get_timestamp
from application.status import ModuleCategory, ModuleStatus, FileSaveMode
from application.suitedir.models import SuiteDir
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.virtualfile.models import VirtualFile
from application.virtualfile.serializers import VirtualFileSerializers, UploadForm
from application.common.ztree.generatenode import handler_suite_node
from application.common.access.projectaccess import has_project_permission
from application.virtualfile.handler import PATH_SEPARATOR
from application.virtualfile.handler import get_file_content, get_full_dir_path, get_download_file_stream

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
        suite = suite_query.first()
        if not has_project_permission(suite.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        full_path_list = get_full_dir_path(suite.suite_dir, [])
        file_name = suite.name
        suffix = str(search(r'\w*(.\w*)', file_name).group(1))
        file_data['file_name'] = file_name
        file_data['file_suffix'] = suffix
        file_data['update_time'] = int(get_timestamp(10))
        file_data['edit_file'] = True
        file_data['file_path'] = PATH_SEPARATOR.join(full_path_list)
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
            id=suite_id,
            status=ModuleStatus.NORMAL
        )
        if not suite_query.exists():
            return JsonResponse(code=10307, msg='not found')
        suite = suite_query.first()
        if not has_project_permission(suite.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
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
        dir_obj = dir_queryset.first()
        if not has_project_permission(dir_obj.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        dir_path = get_full_dir_path(dir_obj, [])
        with transaction.atomic():
            for f in files:
                if f.size > settings.FILE_SIZE_LIMIT:
                    continue
                suffix = str(search(r'\w*(.\w*)', f.name).group(1))
                related_suite_data = {
                    'project_id': dir_obj.project_id,
                    'category': ModuleCategory.FILE,
                    'create_by': request.user.email
                }
                suite, created = TestSuite.objects.update_or_create(
                    name=f.name,
                    suite_dir_id=dir_id,
                    defaults=related_suite_data
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
        suite_query = TestSuite.objects.filter(
            id=suite_id,
            status=ModuleStatus.NORMAL
        )
        if not suite_query.exists():
            return JsonResponse(code=10307, msg='file not found')
        if not has_project_permission(suite_query.first().project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        file_query = VirtualFile.objects.filter(
            suite_id=suite_id,
            status=ModuleStatus.NORMAL
        )
        if not file_query.exists():
            return JsonResponse(code=10307, msg='file not found')
        instance = file_query.first()
        file_path = Path(settings.PROJECT_FILES, instance.file_path)
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
        return open(file, 'rb')


class InternalFileViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def download_file(self, request, *args, **kwargs):
        logger.info(f'接受slaver下载请求: {request.data}')
        auth = request.headers.get('auth')
        if auth != base64_encrypt(settings.INTERNAL_KEY):
            return HttpResponse('FORBIDDEN', status=403)
        path_str = request.data.get('path')
        file_name = request.data.get('name')
        if not path_str or path_str.strip() == '':
            return HttpResponse('404_NOT_FOUND', status=404)
        file = get_download_file_stream(path_str, file_name)
        if not file:
            return HttpResponse('404_NOT_FOUND', status=404)
        response = FileResponse(file)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
        response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response

